#app/services.py
from typing import Optional, List
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
# ИЗМЕНЕНО: Добавлен импорт cast и String для поиска по дате
from sqlalchemy import select, delete, update, cast, String

from .models import Advertisement as AdModel
from .schemas import AdvertResponse, CreateAdvertRequest, UpdateAdvertRequest


# Создание объявления
async def create_advert(
    session: AsyncSession,
    data: CreateAdvertRequest
) -> AdvertResponse:
    advert = AdModel(**data.model_dump())
    try:
        session.add(advert)
        await session.commit()
        await session.refresh(advert)  # Добавлено: получаем актуальное состояние (например, сгенерированный id)
        return AdvertResponse.model_validate(advert) 
    except IntegrityError:
        await session.rollback()  # Добавлено: обязательно откатываем транзакцию, чтобы не "отравить" сессию
        raise HTTPException(409, detail="Ошибка при создании объявления.")


# Получение по ID
async def get_advert_by_id(session: AsyncSession, ad_id: int) -> AdvertResponse:
    stmt = select(AdModel).where(AdModel.id == ad_id)
    result = await session.execute(stmt)
    advert = result.scalar_one_or_none()
    if not advert:
        raise HTTPException(status_code=404, detail=f'Объявление {ad_id} не найдено.')
    return AdvertResponse.model_validate(advert)  


# Обновление
# ИЗМЕНЕНО: Исправлен подход на "get -> setattr -> commit"
async def patch_advert(
    session: AsyncSession,
    ad_id: int,
    data: UpdateAdvertRequest
) -> AdvertResponse:
    advert = await session.get(AdModel, ad_id)
    
    if not advert:
        raise HTTPException(status_code=404, detail=f'Объявление {ad_id} не найдено.')
    
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(advert, field, value)
        
    await session.commit()
    await session.refresh(advert)
    return AdvertResponse.model_validate(advert)   


# Удаление
async def delete_advert(session: AsyncSession, ad_id: int) -> None:
    # 1. Пытаемся получить объект из БД по первичному ключу
    advert = await session.get(AdModel, ad_id)
    
    # 2. Если объекта нет - возвращаем 404
    if not advert:
        raise HTTPException(status_code=404, detail=f'Объявление {ad_id} не найдено.')
    
    # 3. Удаляем объект через ORM-сессию
    await session.delete(advert)
    await session.commit()


# Поиск
# ИЗМЕНЕНО (пункт 2, 3): Добавлены query_description и query_created_at, переименованы параметры (убран префикс q_)
async def search_adverts(
    session: AsyncSession,
    query_title: Optional[str] = None,
    query_author: Optional[str] = None,
    query_price_min: Optional[float] = None,
    query_price_max: Optional[float] = None,
    query_description: Optional[str] = None,
    query_created_at: Optional[str] = None) -> List[AdvertResponse]:
    stmt = select(AdModel)

    # Фильтры
    if query_title is not None:
        stmt = stmt.where(AdModel.title.ilike(f'%{query_title}%'))

    if query_author is not None:
        stmt = stmt.where(AdModel.author.ilike(f'%{query_author}%'))

    if query_price_min is not None:
        stmt = stmt.where(AdModel.price >= query_price_min)

    if query_price_max is not None:
        stmt = stmt.where(AdModel.price <= query_price_max)
        
    # ИЗМЕНЕНО (пункт 2): Добавлен поиск по description
    if query_description is not None:
        stmt = stmt.where(AdModel.description.ilike(f'%{query_description}%'))
        
    # ИЗМЕНЕНО (пункт 2): Добавлен поиск по created_at (через приведение к строке для частичного совпадения)
    if query_created_at is not None:
        stmt = stmt.where(cast(AdModel.created_at, String).ilike(f'%{query_created_at}%'))
