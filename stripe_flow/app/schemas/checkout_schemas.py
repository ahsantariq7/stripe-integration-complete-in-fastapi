from pydantic import BaseModel
from typing import Optional


class CheckoutSessionCreate(BaseModel):
    success_url: str
    cancel_url: str
    mode: str
    customer_email: Optional[str] = None
    quantity: int = 1


class CheckoutSessionResponse(BaseModel):
    checkout_url: str
    session_id: str
    price_id: Optional[str] = None
