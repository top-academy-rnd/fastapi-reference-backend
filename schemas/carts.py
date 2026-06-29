from pydantic import BaseModel


class CartItemResponse(BaseModel):
    id: int
    product_id: int


class CartItemCreate(BaseModel):
    product_id: int
