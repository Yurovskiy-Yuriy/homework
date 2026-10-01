#app/schemas.py
from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from typing import Optional

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    token: str
    model_config = ConfigDict(from_attributes=True)

class CreateUserRequest(BaseModel):
    username: str
    password: str

class UpdateUserRequest(BaseModel):
    username: str | None = None
    password: str | None = None

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    
    model_config = ConfigDict(from_attributes=True)

    # ДОРАБОТКА: Учим Pydantic извлекать имя роли из объекта Role
    @field_validator('role', mode='before')
    @classmethod
    def extract_role_name(cls, value):
        if hasattr(value, 'name'):
            return value.name
        return value

class CreateAdvertRequest(BaseModel):
    title: str
    description: str
    price: float
    author: str

class UpdateAdvertRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    author: str | None = None

class AdvertResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float
    author: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CreateAdvertResponse(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)