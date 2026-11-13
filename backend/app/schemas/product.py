from typing import Any

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str
    category: str
    price: float = Field(ge=0)
    currency: str = "INR"
    features: list[str] = Field(default_factory=list)
    target_audience: dict[str, Any] | None = None


class Product(ProductCreate):
    product_id: str
