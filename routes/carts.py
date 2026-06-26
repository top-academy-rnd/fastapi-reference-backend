from typing import Annotated

from fastapi import APIRouter, Header

from schemas.users import LoginData

router = APIRouter()


# пример HTTP запроса (обратите внимание что данные входа переданы в заголовках запроса, не в теле)
'''
GET /users/5/cart/items
Login: mihail
Password: grhebd
'''


@router.get("/users/{user_id}/cart/items")
async def get_cart(
        user_id: int,
        login: Annotated[str, Header()],
        password: Annotated[str, Header()],
):
    # Идентификация
    # 1. получить пользователя по логину
    # Авторизация
    # 2. проверить пароль
    # Аутентификация запроса пользователя
    # 3. проверить что пользователь запрашивает свою корзину
    # Выполнить запрос
    # 4. получить элементы в корзине
    # 5. вернуть ответ на запрос

    # Обратите внимание, что на многих этапах могут возникнуть ситуации, при которых нужно прекратить обраьатывать запрос и вернуть правильный HTTP ответ с ошибкой.

    pass

