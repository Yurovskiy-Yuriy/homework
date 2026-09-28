# app/app.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from .config import config
from .models import Base 
from pydantic import BaseModel, ConfigDict
from .services import (
    create_advert,
    get_advert_by_id,
    patch_advert,
    delete_advert,
    search_adverts
)
from .schemas import CreateAdvertRequest, UpdateAdvertRequest, AdvertResponse, CreateAdvertResponse

# Создаем асинхронный движок. 
# pool_pre_ping=True защищает от обрыва соединения с БД при долгом простое контейнера.
engine = create_async_engine(config.DATABASE_URL, echo=False, pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

# Зависимость для получения сессии базы данных в эндпоинтах
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# app = FastAPI(lifespan=lifespan)
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    from .models import Base  # Импортируем здесь, чтобы гарантировать загрузку моделей
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def on_shutdown():
    await engine.dispose()


@app.post('/v1/advertisement', response_model=CreateAdvertResponse)
async def api_create_advert(
    data: CreateAdvertRequest,
    db: AsyncSession = Depends(get_db)
):
    """Создание нового объявления"""
    try:
        new_advert = await create_advert(db, data)
        return CreateAdvertResponse(id=new_advert.id)
    except HTTPException as e:
        if e.status_code == 409:
            raise HTTPException(status_code=409, detail="Объявление с такими данными уже существует.")
        raise


@app.get('/v1/advertisement/{advert_id}', response_model=AdvertResponse)
async def api_get_advert(
    advert_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Получить объявление по ID"""
    return await get_advert_by_id(db, advert_id)


@app.patch('/v1/advertisement/{advert_id}', response_model=AdvertResponse)
async def api_patch_advert(
    advert_id: int,
    data: UpdateAdvertRequest,
    db: AsyncSession = Depends(get_db)
):
    """Частичное обновление объявления"""
    return await patch_advert(db, advert_id, data)


@app.delete('/v1/advertisement/{advert_id}')
async def api_delete_advert(
    advert_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Удаление объявления"""
    await delete_advert(db, advert_id)
    return {"status": "ok"}


@app.get('/v1/advertisement', response_model=list[AdvertResponse])
async def api_search_adverts(
    q_title: str | None = None,
    q_author: str | None = None,
    q_price_min: float | None = None,
    q_price_max: float | None = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Поиск объявлений по параметрам:
    ?q_title=машина&q_author=Иван&q_price_min=10000&q_price_max=50000
    """
    adverts = await search_adverts(db, q_title, q_author, q_price_min, q_price_max)
    return adverts