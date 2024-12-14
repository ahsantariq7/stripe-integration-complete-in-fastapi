from fastapi import APIRouter
from app.services.product_service import ProductService
from app.schemas.product_schemas import (
    ProductResponse,
    ProductListResponse,
    PriceListResponse,
    ProductCreateRequest,
    ProductCreateResponse,
)

router = APIRouter()


@router.get("/products", response_model=ProductListResponse)
async def list_products():
    """List all active products"""
    return await ProductService.list_products()


@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    """Get a specific product details"""
    return await ProductService.get_product(product_id)


@router.get("/prices/{product_id}", response_model=PriceListResponse)
async def get_product_prices(product_id: str):
    """Get all prices for a specific product"""
    return await ProductService.get_product_prices(product_id)


@router.post("/products", response_model=ProductCreateResponse)
async def create_product(product_data: ProductCreateRequest):
    """Create a new product with price in Stripe"""
    return await ProductService.create_product(
        name=product_data.name,
        description=product_data.description,
        amount=product_data.amount,
        price_type=product_data.price_type,
        currency=product_data.currency,
        interval=product_data.interval,
        metadata=product_data.metadata,
    )
