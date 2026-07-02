from typing import Annotated

from argon2 import PasswordHasher
from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_session
from models import User
from schemas.users import UserCreate, UserResponse

router = APIRouter()


@router.post("/users")
async def create_user(
        user_data: Annotated[UserCreate, Body()],
        session: Annotated[AsyncSession, Depends(get_session)],
):
    ph = PasswordHasher()
    password_hash = ph.hash(user_data.password)

    new_user = User(
        login=user_data.login,
        password_hash=password_hash,
    )
    session.add(new_user)
    await session.commit()

    return UserResponse(
        id=new_user.id,
        login=new_user.login,
    )
