import os
import stripe
from fastapi import HTTPException
from app.schemas.session_schemas import SessionResponse, SessionDetailsResponse
from app.schemas.checkout_schemas import CheckoutSessionCreate, CheckoutSessionResponse
from app.core.config import settings

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


class SessionService:
    @staticmethod
    async def get_session(session_id: str) -> SessionResponse:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            return SessionResponse(
                status=session.status,
                customer_email=session.customer_email,
                amount_total=session.amount_total,
                currency=session.currency,
                payment_status=session.payment_status,
            )
        except stripe.error.StripeError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def get_session_details(session_id: str) -> SessionDetailsResponse:
        try:
            session = stripe.checkout.Session.retrieve(
                session_id, expand=["customer", "payment_intent", "subscription"]
            )

            response_data = {
                "status": session.status,
                "customer_email": session.customer_email,
                "amount_total": session.amount_total,
                "currency": session.currency,
                "payment_status": session.payment_status,
                "customer_details": session.customer_details,
            }

            if session.payment_intent:
                response_data["payment_details"] = {
                    "payment_id": session.payment_intent.id,
                    "payment_method": session.payment_intent.payment_method,
                    "payment_method_types": session.payment_intent.payment_method_types,
                    "created": session.payment_intent.created,
                }

            if session.subscription:
                response_data["subscription_details"] = {
                    "subscription_id": session.subscription.id,
                    "current_period_start": session.subscription.current_period_start,
                    "current_period_end": session.subscription.current_period_end,
                    "status": session.subscription.status,
                }

            return SessionDetailsResponse(**response_data)

        except stripe.error.StripeError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def create_checkout_session(
        checkout_data: CheckoutSessionCreate, price_id: str
    ) -> CheckoutSessionResponse:
        try:
            # First, get the price to check its type
            price = await stripe.Price.retrieve(price_id)

            # Check price type
            mode = "payment" if price.type == "one_time" else "subscription"

            session = await stripe.checkout.Session.create(
                success_url=f"{settings.BASE_URL}{settings.STRIPE_SUCCESS_URL}?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{settings.BASE_URL}{settings.STRIPE_CANCEL_URL}?session_id={{CHECKOUT_SESSION_ID}}",
                mode=mode,  # Will be "payment" for one_time, "subscription" for recurring
                line_items=[{"price": price_id, "quantity": checkout_data.quantity}],
                customer_email=checkout_data.customer_email,
            )

            return CheckoutSessionResponse(
                checkout_url=session.url, session_id=session.id, price_id=price_id
            )
        except stripe.error.StripeError as e:
            print(f"Stripe Error: {str(e)}")  # For debugging
            raise HTTPException(status_code=400, detail=str(e))
