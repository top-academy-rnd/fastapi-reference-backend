from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from models import User, CartItem
from schemas.carts import CartItemResponse, CartItemCreate
from dependencies import get_session, get_authenticated_user

router = APIRouter()


# пример HTTP запроса (обратите внимание, что данные входа переданы в заголовках запроса, не в теле)
'''
GET /users/10/cart/items
Login: mihail
Password: grhebd
'''


@router.get(
    "/users/{user_id}/cart/items",
    response_model=list[CartItemResponse],
)
async def get_cart_items(
        user_id: int,
        authenticated_user: Annotated[User, Depends(get_authenticated_user)],
        session: Annotated[AsyncSession, Depends(get_session)],
):
    # Авторизация запроса пользователя
    # 3. проверить что пользователь запрашивает свою корзину
    if authenticated_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    # Выполнить запрос

    # 4. получить элементы в корзине
    stmt = (select(CartItem)
            .where(CartItem.user_id == user_id))
    cart_items = await session.scalars(stmt)

    # 5. вернуть ответ на запрос
    result = []
    for i in cart_items:
        result.append(CartItemResponse(
            product_id=i.product_id,
        ))

    return result


async def create_cart_item(
        user_id: int,
        authenticated_user: Annotated[User, Depends(get_authenticated_user)],
        session: Annotated[AsyncSession, Depends(get_session)],
        payload: Annotated[CartItemCreate, Body()],
):
    if authenticated_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    new_cart_item = CartItem(
        user_id=user_id,
        product_id=payload.product_id,
    )
    session.add(new_cart_item)
    await session.commit()

    result = CartItemResponse(
        id=new_cart_item.id,
        product_id=new_cart_item.product_id,
    )
    return result
