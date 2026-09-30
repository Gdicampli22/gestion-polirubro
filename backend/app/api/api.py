from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.base import Product, Tenant
from app.schemas.schemas import (
    ProductCreate,
    ProductResponse,
    TenantCreate,
    TenantResponse,
)


router = APIRouter()


@router.post(
    "/tenants/",
    response_model=TenantResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_tenant(
    tenant_data: TenantCreate,
    db: Session = Depends(get_db),
) -> Tenant:
    tenant = Tenant(**tenant_data.model_dump())
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant


@router.get("/tenants/", response_model=list[TenantResponse])
def list_tenants(db: Session = Depends(get_db)) -> list[Tenant]:
    return db.query(Tenant).order_by(Tenant.id).all()


@router.post(
    "/products/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
) -> Product:
    tenant = db.get(Tenant, product_data.tenant_id)
    if tenant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe el comercio indicado.",
        )

    product = Product(**product_data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/products/", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db)) -> list[Product]:
    return db.query(Product).order_by(Product.id).all()