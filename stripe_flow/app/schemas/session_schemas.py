from pydantic import BaseModel
from typing import Optional, Dict, List


class SessionResponse(BaseModel):
    status: str
    customer_email: Optional[str]
    amount_total: int
    currency: str
    payment_status: str


class PaymentDetails(BaseModel):
    payment_id: str
    payment_method: Optional[str]
    payment_method_types: List[str]
    created: int


class SubscriptionDetails(BaseModel):
    subscription_id: str
    current_period_start: int
    current_period_end: int
    status: str


class SessionDetailsResponse(SessionResponse):
    customer_details: Optional[Dict] = None
    payment_details: Optional[PaymentDetails] = None
    subscription_details: Optional[SubscriptionDetails] = None
