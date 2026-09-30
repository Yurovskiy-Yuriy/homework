#app/schemas.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CreateAdvertRequest(BaseModel):
    title: str
     # ИЗМЕНЕНО: Поле description сделано обязательным (убрано | None)
    description: str
    price: float
    author: str

class UpdateAdvertRequest(BaseModel):
    title: str | None
    description: str | None
    price: float | None
    author: str | None

class AdvertResponse(BaseModel):
    id: int
    title: str
    # ИЗМЕНЕНО: Поле description сделано обязательным (убрано | None)
    description: str
    # ИЗМЕНЕНО: Тип цены float
    price: float
    author: str
    created_at: datetime

    class Config:
        from_attributes = True

class CreateAdvertResponse(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)