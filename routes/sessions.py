from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Body, Header
from pydantic import BaseModel
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from models import User, CartItem, LoginSession
from schemas.carts import CartItemResponse, CartItemCreate
from dependencies import get_session, get_authenticated_user
from uuid import uuid4


router = APIRouter()


class LoginSessionResponse(BaseModel):
    user_id: int
    secret: str


@router.post(
    "/sessions",
    response_model=LoginSessionResponse,
)
async def create_session(
        login: Annotated[str, Header()],
        password: Annotated[str, Header()],
        session: Annotated[AsyncSession, Depends(get_session)],
):
    # Идентификация
    # 1. получить пользователя по логину
    stmt = select(User).where(User.login == login)
    user = await session.scalar(stmt)
    if user is None:
        raise HTTPException(status_code=401, detail="Authenticated")

    # Аутентификация
    # 2. проверить пароль
    if user.password != password:
        raise HTTPException(status_code=401, detail="Authenticated")

    # Создаём сессию в БД
    new_login_session = LoginSession(
        user_id=user.id,
        secret=str(uuid4()),
    )
    session.add(new_login_session)
    await session.commit()

    return LoginSessionResponse(
        user_id=new_login_session.user_id,
        secret=new_login_session.secret,
    )
