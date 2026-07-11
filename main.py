from uvicorn import run

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import users, carts, products, sessions


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_headers="*",
    allow_origins="*",
    allow_methods="*",
)


app.include_router(users.router)
app.include_router(carts.router)
app.include_router(products.router)
app.include_router(sessions.router)


run(app)
