#app/services.py
from typing import Optional, List
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, cast, String
import bcrypt
import datetime

from .models import Advertisement as AdModel, User, Role, Token
from .schemas import (
    AdvertResponse, CreateAdvertRequest, UpdateAdvertRequest,
    UserResponse, CreateUserRequest, UpdateUserRequest
)
from .config import config

# Утилиты для работы с паролями
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

# Аутентификация (Логин)
async def login_user(session: AsyncSession, username: str, password: str) -> Token:
    stmt = select(User).where(User.username == username)
    user = await session.scalar(stmt)
    
    if not user or not check_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Неверное имя пользователя или пароль")
    
    # Создаем новый токен
    new_token = Token(user_id=user.id)
    session.add(new_token)
    await session.commit()
    await session.refresh(new_token)
    return new_token

# CRUD для пользователей
async def create_user_service(session: AsyncSession, data: CreateUserRequest) -> UserResponse:
    # Проверяем, существует ли пользователь
    stmt = select(User).where(User.username == data.username)
    if await session.scalar(stmt):
        raise HTTPException(status_code=409, detail="Пользователь с таким именем уже существует")
    
    # Находим роль 'user' по умолчанию
    role_stmt = select(Role).where(Role.name == 'user')
    user_role = await session.scalar(role_stmt)
    if not user_role:
        raise HTTPException(status_code=500, detail="Роль 'user' не найдена в БД")

    new_user = User(
        username=data.username,
        password_hash=hash_password(data.password),
        role_id=user_role.id
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return UserResponse.model_validate(new_user)

async def get_user_service(session: AsyncSession, user_id: int) -> UserResponse:
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return UserResponse.model_validate(user)

async def update_user_service(session: AsyncSession, user_id: int, data: UpdateUserRequest, current_user: User) -> UserResponse:
    # Проверка прав (только админ или сам пользователь)
    if current_user.role.name != 'admin' and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Недостаточно прав для изменения чужих данных")

    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    update_data = data.model_dump(exclude_unset=True)
    if 'password' in update_data:
        update_data['password_hash'] = hash_password(update_data.pop('password'))
    if 'username' in update_data:
        # Проверка на уникальность нового имени
        stmt = select(User).where(User.username == update_data['username'], User.id != user_id)
        if await session.scalar(stmt):
            raise HTTPException(status_code=409, detail="Это имя пользователя уже занято")

    for field, value in update_data.items():
        setattr(user, field, value)
        
    await session.commit()
    await session.refresh(user)
    return UserResponse.model_validate(user)

async def delete_user_service(session: AsyncSession, user_id: int, current_user: User) -> dict:
    # Проверка прав (только админ или сам пользователь)
    if current_user.role.name != 'admin' and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Недостаточно прав для удаления чужих данных")

    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    await session.delete(user)
    await session.commit()
    return {"status": "ok"}


# --- Существующие сервисы с ДОРАБОТКАМИ для проверки прав ---

async def create_advert(
    session: AsyncSession,
    data: CreateAdvertRequest,
    current_user: User # Передаем текущего пользователя
) -> AdvertResponse:
    advert = AdModel(
        title=data.title,
        description=data.description,
        price=data.price,
        author=data.author,
        author_id=current_user.id # Привязываем объявление к создателю
    )
    try:
        session.add(advert)
        await session.commit()
        await session.refresh(advert)
        return AdvertResponse.model_validate(advert) 
    except IntegrityError:
        await session.rollback()
        raise HTTPException(409, detail="Ошибка при создании объявления.")

async def get_advert_by_id(session: AsyncSession, ad_id: int) -> AdvertResponse:
    stmt = select(AdModel).where(AdModel.id == ad_id)
    result = await session.execute(stmt)
    advert = result.scalar_one_or_none()
    if not advert:
        raise HTTPException(status_code=404, detail=f'Объявление {ad_id} не найдено.')
    return AdvertResponse.model_validate(advert)  

async def patch_advert(
    session: AsyncSession,
    ad_id: int,
    data: UpdateAdvertRequest,
    current_user: User # Передаем текущего пользователя для проверки прав
) -> AdvertResponse:
    advert = await session.get(AdModel, ad_id)
    if not advert:
        raise HTTPException(status_code=404, detail=f'Объявление {ad_id} не найдено.')
    
    # Проверка прав (админ или владелец объявления)
    if current_user.role.name != 'admin' and advert.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Недостаточно прав для изменения чужого объявления")
    
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(advert, field, value)
        
    await session.commit()
    await session.refresh(advert)
    return AdvertResponse.model_validate(advert)   

async def delete_advert(session: AsyncSession, ad_id: int, current_user: User) -> None:
    advert = await session.get(AdModel, ad_id)
    if not advert:
        raise HTTPException(status_code=404, detail=f'Объявление {ad_id} не найдено.')
    
    # Проверка прав (админ или владелец объявления)
    if current_user.role.name != 'admin' and advert.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Недостаточно прав для удаления чужого объявления")
    
    await session.delete(advert)
    await session.commit()

async def search_adverts(
    session: AsyncSession,
    query_title: Optional[str] = None,
    query_author: Optional[str] = None,
    query_price_min: Optional[float] = None,
    query_price_max: Optional[float] = None,
    query_description: Optional[str] = None,
    query_created_at: Optional[str] = None
) -> List[AdvertResponse]:
    stmt = select(AdModel)

    if query_title is not None:
        stmt = stmt.where(AdModel.title.ilike(f'%{query_title}%'))
    if query_author is not None:
        stmt = stmt.where(AdModel.author.ilike(f'%{query_author}%'))
    if query_price_min is not None:
        stmt = stmt.where(AdModel.price >= query_price_min)
    if query_price_max is not None:
        stmt = stmt.where(AdModel.price <= query_price_max)
    if query_description is not None:
        stmt = stmt.where(AdModel.description.ilike(f'%{query_description}%'))
    if query_created_at is not None:
        stmt = stmt.where(cast(AdModel.created_at, String).ilike(f'%{query_created_at}%'))

    result = await session.execute(stmt)
    adverts = result.scalars().all()
    return [AdvertResponse.model_validate(adv) for adv in adverts]