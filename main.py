import os
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import db, create_document, get_documents
from schemas import Order, Message, Affiliate, CreatedResponse

app = FastAPI(title="SaaS Landing API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Backend OK"}

@app.get("/test")
def test_database():
    info = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": bool(os.getenv("DATABASE_URL")),
        "database_name": bool(os.getenv("DATABASE_NAME")),
        "collections": []
    }
    try:
        if db is not None:
            info["database"] = "✅ Connected"
            try:
                info["collections"] = db.list_collection_names()
            except Exception as e:
                info["database"] = f"⚠️ Connected with warning: {str(e)[:80]}"
    except Exception as e:
        info["database"] = f"❌ Error: {str(e)[:80]}"
    return info

# Orders
@app.post("/orders", response_model=CreatedResponse)
def create_order(order: Order):
    try:
        order_id = create_document("order", order)
        return CreatedResponse(id=order_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/orders")
def list_orders(limit: int = 50):
    try:
        docs = get_documents("order", {}, limit)
        # Serialize ObjectId
        out = []
        for d in docs:
            d["id"] = str(d.get("_id"))
            d.pop("_id", None)
            out.append(d)
        return out
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Messages
@app.post("/messages", response_model=CreatedResponse)
def create_message(msg: Message):
    try:
        msg_id = create_document("message", msg)
        return CreatedResponse(id=msg_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Affiliates
@app.post("/affiliates", response_model=CreatedResponse)
def create_affiliate(aff: Affiliate):
    try:
        aff_id = create_document("affiliate", aff)
        return CreatedResponse(id=aff_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
