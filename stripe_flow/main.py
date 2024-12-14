import uvicorn
import stripe
from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import product_routes, checkout_routes, session_routes

app = FastAPI()

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# Include routers
app.include_router(
    product_routes.router, prefix="/stripe-product", tags=["Stripe Product"]
)
app.include_router(
    checkout_routes.router, prefix="/stripe-checkout", tags=["Stripe Checkout"]
)
app.include_router(
    session_routes.router, prefix="/stripe-session", tags=["Stripe Session"]
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
