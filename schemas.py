from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

class OrderItem(BaseModel):
    name: str = Field(..., description="Nom du plan ou produit")
    price: float = Field(..., ge=0)
    quantity: int = Field(1, ge=1)

class Order(BaseModel):
    customer_name: str = Field(..., description="Nom complet")
    customer_email: EmailStr
    plan: str = Field(..., description="Identifiant du plan choisi")
    items: List[OrderItem] = Field(default_factory=list)
    notes: Optional[str] = None

class Message(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

class Affiliate(BaseModel):
    name: str
    email: EmailStr
    website: Optional[str] = None
    audience: Optional[str] = Field(None, description="Description de l'audience")

class CreatedResponse(BaseModel):
    id: str
    status: str = "created"
