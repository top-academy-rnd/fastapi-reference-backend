from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


engine = create_async_engine(
    "postgresql+asyncpg://postgres:postgres@127.0.0.1/postgres",
    echo=True,
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    age: Mapped[int | None]


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[int]


class CartItem(Base):
    __tablename__ = "cart_item"

    id: Mapped[int] = mapped_column(primary_key=True)

    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))


class LoginSession(Base):
    __tablename__ = "login_session"

    id: Mapped[int] = mapped_column(primary_key=True)
    secret: Mapped[str]
    expires_at: Mapped[datetime]

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
