import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.database.session import get_session
from backend.app.models.orm import ProductORM
from backend.app.schemas.product import Product, ProductCreate

router = APIRouter(prefix="/products", tags=["products"])


def _out(p: ProductORM) -> Product:
    return Product(
        product_id=p.product_id, name=p.name, description=p.description, category=p.category,
        price=p.price, currency=p.currency, features=p.features or [], target_audience=p.target_audience,
    )


@router.post("", response_model=Product, status_code=201)
async def create_product(body: ProductCreate, s: AsyncSession = Depends(get_session)):
    p = ProductORM(product_id=f"PROD{uuid.uuid4().hex[:8].upper()}", **body.model_dump())
    s.add(p)
    await s.commit()
    return _out(p)


@router.get("", response_model=list[Product])
async def list_products(s: AsyncSession = Depends(get_session)):
    rows = (await s.execute(select(ProductORM).order_by(ProductORM.created_at.desc()))).scalars().all()
    return [_out(p) for p in rows]


@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: str, s: AsyncSession = Depends(get_session)):
    p = await s.get(ProductORM, product_id)
    if p is None:
        raise HTTPException(404, "Product not found")
    return _out(p)
