from fastapi import FastAPI
from app.api.routes import product_routes, checkout_routes, session_routes

def create_app():
    app = FastAPI(title="Stripe Flow API")
    
    # Include routers
    app.include_router(product_routes.router, tags=["Products"])
    app.include_router(checkout_routes.router, tags=["Checkout"])
    app.include_router(session_routes.router, tags=["Sessions"])
    
    return app
