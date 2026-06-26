from typing import Annotated

from fastapi import APIRouter, Header

from schemas.users import LoginData

router = APIRouter()


@router.get("/users/{user_id}/cart/items")
async def get_cart(
        user_id: int,
        login_data: Annotated[LoginData, Header()]
):
    # получить пользователя по логину
    # проверить пароль
    # получить элементы в корзине
    # вернуть результат

    # Идентификация
    # Аутентификация
    # Авторизация
    pass


'''
GET /users/5/cart/items
Login: mihail
Password: grhebd
'''
