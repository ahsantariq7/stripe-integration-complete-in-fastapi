from fastapi import APIRouter, Form
from typing import Optional
from app.services.checkout_service import CheckoutService
from app.schemas.checkout_schemas import CheckoutSessionResponse

router = APIRouter()

@router.post("/create-from-product/{product_id}", response_model=CheckoutSessionResponse)
async def create_checkout_from_product(
    product_id: str,
    success_url: str = Form(...),
    cancel_url: str = Form(...),
    mode: str = Form(...),
    customer_email: Optional[str] = Form(None),
    quantity: int = Form(1),
):
    """Create a checkout session from a product ID"""
    return await CheckoutService.create_checkout_from_product(
        product_id=product_id,
        success_url=success_url,
        cancel_url=cancel_url,
        mode=mode,
        customer_email=customer_email,
        quantity=quantity,
    )

@router.post("/create-from-price/{price_id}", response_model=CheckoutSessionResponse)
async def create_checkout_from_price(
    price_id: str,
    success_url: str = Form(...),
    cancel_url: str = Form(...),
    customer_email: Optional[str] = Form(None),
    quantity: int = Form(1),
):
    """Create a checkout session directly from a price ID"""
    return await CheckoutService.create_checkout_from_price(
        price_id=price_id,
        success_url=success_url,
        cancel_url=cancel_url,
        customer_email=customer_email,
        quantity=quantity,
    ) 