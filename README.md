Это референсный бэкенд

# Cheatsheet

## Установить все нужные python библиотеки

```bash
uv sync
```


## Запустить веб-сервер (программа, обрабатывающая HTTP запросы)

```bash
uv run main.py
```

Однако чтобы всё работало у вас должен быть запущен PostgreSQL, и 
веб-сервер должен быть способен у нему подключиться.

## Запустить миграции, ещё не применённые к базе данных

```bash
uv run alembic upgrade head
```

## Сгенерировать новую миграцию исходя из состояния БД и моделей в коде

```bash
uv run alembic revision -m "Migration name" --autogenerate 
```

## Запустить тесты

```bash
uv run pytest tests
```

Примечание: при этом pytest сам возьмём оттуда все файлы которые начинаются с 
`test`, например `test_users.py`, и соберёт с них все функции которые 
начинаются с `test`, например `test_registration`.


# Технологический стек

* Uvicorn
* FastAPI
* SQLAlchemy (ORM)
* Asyncpg
* PostgreSQL
* Alembic

# Предметная область


Интернет-магазин.

Есть доступные товары.  Есть пользователи, у каждого пользователя есть корзина.

Какие взаимодействия поддерживаются:
* Регистрация пользователя
* Получение списка товаров
* Добавление товара в корзину (разрешено только владельцу корзины)

# Структура исходного кода

Маршруты FastAPI находятся в папке `routes` разделены по смыслу на относящиеся к
1. Пользователям
2. Корзинам
3. Товарам

Схемы API разделены так же, находятся в `schemas`.

В названии классов схем сначала указывается модель о которой говорим (например User), затем контекст в котором мы используем эту модель (например Create или Response).

Модели SQLAlchemy находятся в `models`.

# Схема работы сервисов (кроме бд)

```mermaid
graph TD
    Browser[Browser]
    
    subgraph Host[Host Machine]
        Port80[Port 80]
        
        subgraph Docker[Docker Network]
            Nginx[Nginx Container<br>Port 80]
            Frontend[Frontend Container<br>Vite/React/Vue<br>Port 5173]
        end
    end

    %% Request Flow
    Browser -->|1. HTTP Request on 80.68.156.37:80 | Port80
    Port80 -->|2. Reverse Proxy| Nginx
    Nginx -->|3. Forward Request to frontend:5173| Frontend
    
    %% Response Flow
    Frontend -->|4. HTTP Response| Nginx
    Nginx -->|5. HTTP Response| Browser

    %% Styling
    style Browser fill:#f9f,stroke:#333,stroke-width:2px
    style Host fill:#e1f5fe,stroke:#0288d1,stroke-width:2px
    style Docker fill:#fffde7,stroke:#fbc02d,stroke-width:2px,stroke-dasharray: 5 5
    style Nginx fill:#85ffc7,stroke:#00c853,stroke-width:2px
    style Frontend fill:#ffcc80,stroke:#f57c00,stroke-width:2px
```