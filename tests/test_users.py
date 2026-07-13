from uuid import uuid4

import requests


def test_registration():
    test_login = f"test-{uuid4()}"
    test_password = str(uuid4())
    r = requests.post(
        "http://127.0.0.1:8000/users",
        json={
            "login": test_login,
            "password": test_password,
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data == {"id": data["id"], "login": test_login}


def get_registered_user():
    """ Регистрирует пользователя, возвращает логин и пароль"""

    test_login = f"test-{uuid4()}"
    test_password = str(uuid4())
    r = requests.post(
        "http://127.0.0.1:8000/users",
        json={
            "login": test_login,
            "password": test_password,
        },
    )
    assert r.status_code == 200  # но в принципе этот assert можно не делать

    data = r.json()
    return test_login, test_password, data["id"]


def test_create_session_incorrect_password():  # проверяем вход с некорректным паролем
    # регистрируете пользователя через функцию
    # на этом пользователе делаете проверку

    test_login, test_password, test_user_id = get_registered_user()

    r = requests.post(
        "http://127.0.0.1:8000/sessions",
        headers={
            "login": test_login,
            "password": test_password + "incorrect",
        },
    )
    assert r.status_code == 401


def test_create_session_correct_password():  # проверяем вход с корректным паролем
    # регистрируете пользователя через функцию
    # на этом пользователе делаете проверку

    pass
