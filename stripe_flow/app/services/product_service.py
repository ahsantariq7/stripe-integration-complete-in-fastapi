import stripe
from fastapi import HTTPException
from typing import Dict, List
from app.schemas.product_schemas import ProductResponse, PriceResponse
import os

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


class ProductService:
    @staticmethod
    async def list_products() -> Dict[str, List[ProductResponse]]:
        try:
            products = stripe.Product.list(active=True)
            return {
                "products": [
                    ProductResponse(
                        id=product.id,
                        name=product.name,
                        description=product.description,
                        images=product.images,
                        default_price=product.default_price,
                        metadata=product.metadata,
                    )
                    for product in products.data
                ]
            }
        except stripe.error.StripeError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def get_product(product_id: str) -> ProductResponse:
        try:
            product = stripe.Product.retrieve(product_id)
            return ProductResponse(
                id=product.id,
                name=product.name,
                description=product.description,
                images=product.images,
                default_price=product.default_price,
                metadata=product.metadata,
            )
        except stripe.error.StripeError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def get_product_prices(product_id: str) -> Dict[str, List[PriceResponse]]:
        try:
            prices = stripe.Price.list(
                product=product_id, active=True, expand=["data.product"]
            )
            return {
                "prices": [
                    PriceResponse(
                        id=price.id,
                        currency=price.currency,
                        unit_amount=price.unit_amount,
                        recurring=(
                            price.recurring if hasattr(price, "recurring") else None
                        ),
                        product_name=price.product.name if price.product else None,
                    )
                    for price in prices.data
                ]
            }
        except stripe.error.StripeError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def create_product(
        name: str,
        description: str,
        amount: int,
        price_type: str,  # "one_time" or "recurring"
        currency: str = "usd",
        interval: str = None,  # Required only if price_type is "recurring"
        metadata: dict = None,
    ) -> Dict[str, dict]:
        try:
            # Validate price type and interval
            if price_type not in ["one_time", "recurring"]:
                raise ValueError("price_type must be either 'one_time' or 'recurring'")

            if price_type == "recurring" and not interval:
                raise ValueError("interval is required for recurring prices")

            if interval and interval not in ["day", "week", "month", "year"]:
                raise ValueError("interval must be one of: day, week, month, year")

            # Create the product
            product = stripe.Product.create(
                name=name, description=description, metadata=metadata or {}
            )

            # Create price based on type
            price_data = {
                "product": product.id,
                "unit_amount": amount,
                "currency": currency,
            }

            if price_type == "recurring":
                price_data["recurring"] = {"interval": interval}

            price = stripe.Price.create(**price_data)

            # Set as default price
            product = stripe.Product.modify(product.id, default_price=price.id)

            return {
                "product": ProductResponse(
                    id=product.id,
                    name=product.name,
                    description=product.description,
                    images=product.images,
                    default_price=product.default_price,
                    metadata=product.metadata,
                ),
                "price": PriceResponse(
                    id=price.id,
                    currency=price.currency,
                    unit_amount=price.unit_amount,
                    recurring=price.recurring if hasattr(price, "recurring") else None,
                    product_name=product.name,
                ),
            }
        except stripe.error.StripeError as e:
            raise HTTPException(status_code=400, detail=str(e))
