from pydantic import BaseModel
from uuid import UUID

class Product(BaseModel):
    id: int
    uuid: UUID
    name: str
    weight: float

    class Config:
        orm_mode = True
        
class ProductCreate(BaseModel):
    name: str
    weight: float