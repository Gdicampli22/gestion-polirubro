from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class TenantBase(BaseModel):
    name: str
    business_type: str


class TenantCreate(TenantBase):
    pass


class TenantResponse(TenantBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ProductBase(BaseModel):
    sku: str
    name: str
    base_price: Decimal
    attributes: dict[str, Any] = Field(default_factory=dict)


class ProductCreate(ProductBase):
    tenant_id: int


class ProductResponse(ProductBase):
    id: int
    tenant_id: int

    model_config = ConfigDict(from_attributes=True)