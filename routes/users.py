from typing import Annotated

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
    new_user = User(
        login=user_data.login,
        password=user_data.password,
    )
    session.add(new_user)
    await session.commit()

    return UserResponse(
        id=new_user.id,
        login=new_user.login,
    )
