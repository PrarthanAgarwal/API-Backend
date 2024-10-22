# app/schemas/base.py
from pydantic import BaseModel

class ItemBase(BaseModel):
    pass

class ItemCreate(ItemBase):
    pass

class ItemInDBBase(ItemBase):
    id: int

    class Config:
        orm_mode = True

