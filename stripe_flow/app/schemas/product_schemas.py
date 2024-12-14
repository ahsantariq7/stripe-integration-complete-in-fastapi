from pydantic import BaseModel
from typing import List, Optional, Dict, Union


class ProductResponse(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    images: Optional[List[str]] = None
    default_price: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


class PriceResponse(BaseModel):
    id: Optional[str] = None
    currency: Optional[str] = None
    unit_amount: Optional[int] = None
    recurring: Optional[Dict[str, Union[str, int, None]]] = None
    product_name: Optional[str] = None


class ProductListResponse(BaseModel):
    products: List[ProductResponse]


class PriceListResponse(BaseModel):
    prices: List[PriceResponse]


from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Union


# Request Schemas
class ProductCreateRequest(BaseModel):
    name: str = Field(..., description="Name of the product")
    description: str = Field(..., description="Description of the product")
    amount: int = Field(..., description="Amount in cents (e.g., 1999 for $19.99)")
    price_type: str = Field(..., description="Type of price: 'one_time' or 'recurring'")
    currency: str = Field(default="usd", description="Currency code (default: usd)")
    interval: Optional[str] = Field(
        None,
        description="Required for recurring prices: 'day', 'week', 'month', or 'year'",
    )
    metadata: Optional[Dict[str, str]] = Field(
        default=None, description="Additional metadata for the product"
    )


class ProductCreateResponse(BaseModel):
    product: ProductResponse
    price: PriceResponse
