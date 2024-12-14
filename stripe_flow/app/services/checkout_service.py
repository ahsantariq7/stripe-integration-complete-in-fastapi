import os
import stripe
from fastapi import HTTPException
from typing import Optional, Dict
from app.schemas.checkout_schemas import CheckoutSessionResponse

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


class CheckoutService:
    @staticmethod
    async def create_checkout_from_product(
        product_id: str,
        success_url: str,
        cancel_url: str,
        mode: str,
        customer_email: Optional[str] = None,
        quantity: int = 1,
    ) -> CheckoutSessionResponse:
        try:
            product = stripe.Product.retrieve(product_id)
            if not product.default_price:
                prices = stripe.Price.list(product=product_id, active=True, limit=1)
                if not prices.data:
                    raise HTTPException(
                        status_code=400, detail="No active price found for this product"
                    )
                price_id = prices.data[0].id
            else:
                price_id = product.default_price

            checkout_data = {
                "line_items": [{"price": price_id, "quantity": quantity}],
                "mode": mode,
                "success_url": success_url,
                "cancel_url": cancel_url,
            }

            if customer_email:
                checkout_data["customer_email"] = customer_email

            session = stripe.checkout.Session.create(**checkout_data)

            return CheckoutSessionResponse(
                checkout_url=session.url,
                session_id=session.id,
                price_id=price_id,
            )

        except stripe.error.StripeError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def create_checkout_from_price(
        price_id: str,
        success_url: str,
        cancel_url: str,
        customer_email: Optional[str] = None,
        quantity: int = 1,
    ) -> CheckoutSessionResponse:
        try:
            price = stripe.Price.retrieve(price_id)
            mode = "subscription" if price.type == "recurring" else "payment"

            checkout_data = {
                "line_items": [{"price": price_id, "quantity": quantity}],
                "mode": mode,
                "success_url": success_url,
                "cancel_url": cancel_url,
            }

            if customer_email:
                checkout_data["customer_email"] = customer_email

            session = stripe.checkout.Session.create(**checkout_data)

            return CheckoutSessionResponse(
                checkout_url=session.url, session_id=session.id
            )

        except stripe.error.StripeError as e:
            raise HTTPException(status_code=400, detail=str(e))
