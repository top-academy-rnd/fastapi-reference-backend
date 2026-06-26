from pydantic import BaseModel


class ProductResponse(BaseModel):
    id: int
    name: str
    price: int


class ProductCreate(BaseModel):
    name: str
    price: int
