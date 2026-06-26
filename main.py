from uvicorn import run

from fastapi import FastAPI

from models import engine, Base
from routes import users, carts, products


app = FastAPI()


@app.post("/create-all")
async def create_all():
    # можно вынести создание и прогнать один раз только
    conn = await engine.connect()
    await conn.run_sync(Base.metadata.create_all)
    await conn.commit()
    await conn.close()


app.include_router(users.router)
app.include_router(carts.router)
app.include_router(products.router)

# 1. Маршруты
# 2. Схемы данных API (pydantic models)
# 3. Модели базы данных (sqlalchemy models)


run(app)
