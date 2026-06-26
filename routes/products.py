from typing import Annotated

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_session
from schemas.products import (
    ProductResponse,
    ProductCreate,
)
from models import Product

router = APIRouter()


@router.post("/products", response_model=ProductResponse)
async def create_product(
        product_data: Annotated[ProductCreate, Body()],
        session: Annotated[AsyncSession, Depends(get_session)],
):
    new_product = Product(
        name=product_data.name,
        price=product_data.price,
    )
    session.add(new_product)
    await session.commit()
    response = ProductResponse(
        id=new_product.id,
        name=new_product.name,
        price=new_product.price,
    )
    return response


@router.get(
    "/products",
    response_model=list[ProductResponse],
)
async def get_all_products():
    pass
