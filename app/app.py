# app/app.py
from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy import select
import uuid
import datetime
from .config import config
from .models import Base, User, Token, Role
from pydantic import BaseModel, ConfigDict
from .services import (
    create_advert, get_advert_by_id, patch_advert, delete_advert, search_adverts,
    login_user, create_user_service, get_user_service, update_user_service, delete_user_service
)
from .schemas import (
    CreateAdvertRequest, UpdateAdvertRequest, AdvertResponse, CreateAdvertResponse,
    LoginRequest, LoginResponse, CreateUserRequest, UpdateUserRequest, UserResponse
)

engine = create_async_engine(config.DATABASE_URL, echo=False, pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Инициализация ролей при старте, если их нет
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Role))
        if not result.scalars().all():
            session.add_all([Role(name="user"), Role(name="admin")])
            await session.commit()

@app.on_event("shutdown")
async def on_shutdown():
    await engine.dispose()


# ЗАВИСИМОСТИ (DEPENDENCIES) ДЛЯ АУТЕНТИФИКАЦИИ И АВТОРИЗАЦИИ

async def get_optional_user(
    x_token: uuid.UUID | None = Header(default=None, alias="x-token"),
    db: AsyncSession = Depends(get_db)
) -> User | None:
    """Возвращает пользователя, если токен валиден. Если токена нет - возвращает None."""
    if not x_token:
        return None
    
    # Проверяем, что токен существует и не просрочен (24 часа)
    expire_threshold = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=config.TOKEN_TTL)
    from sqlalchemy.sql import func
    db_expire_threshold = func.now() - datetime.timedelta(seconds=config.TOKEN_TTL)
    
    query = select(Token).where(
        Token.token == x_token,
        Token.creation_time >= db_expire_threshold
    )
    token_obj = await db.scalar(query)
    
    if not token_obj:
        raise HTTPException(status_code=401, detail="Неверный или просроченный токен")
    
    return token_obj.user

async def require_auth(user: User | None = Depends(get_optional_user)) -> User:
    """Требует обязательной аутентификации."""
    if not user:
        raise HTTPException(status_code=401, detail="Требуется аутентификация")
    return user

async def require_admin(user: User = Depends(require_auth)) -> User:
    """Требует роль администратора."""
    if user.role.name != 'admin':
        raise HTTPException(status_code=403, detail="Недостаточно прав: требуется роль admin")
    return user

async def require_ownership_user(
    user_id: int,
    user: User = Depends(require_auth)
) -> User:
    """Требует, чтобы пользователь был админом или владел профилем."""
    if user.role.name == 'admin' or user.id == user_id:
        return user
    raise HTTPException(status_code=403, detail="Недостаточно прав: можно изменять только свои данные")

async def require_ownership_advert(
    advert_id: int,
    user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Требует, чтобы пользователь был админом или создателем объявления."""
    if user.role.name == 'admin':
        return user
    
    from .models import Advertisement as AdModel
    advert = await db.get(AdModel, advert_id)
    if advert and advert.author_id == user.id:
        return user
        
    raise HTTPException(status_code=403, detail="Недостаточно прав: можно изменять только свои объявления")


# РОУТЫ АУТЕНТИФИКАЦИИ И ПОЛЬЗОВАТЕЛЕЙ

# Роут для логина (доступен всем)
@app.post('/login', response_model=LoginResponse)
async def api_login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    token_obj = await login_user(db, data.username, data.password)
    return LoginResponse(token=str(token_obj.token))

# Создание пользователя (доступно неавторизованным)
@app.post('/user', response_model=UserResponse)
async def api_create_user(
    data: CreateUserRequest,
    db: AsyncSession = Depends(get_db)
):
    return await create_user_service(db, data)

# Получение пользователя по ID (доступно неавторизованным)
@app.get('/user/{user_id}', response_model=UserResponse)
async def api_get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await get_user_service(db, user_id)

# Обновление пользователя (только авторизованный владелец или админ)
@app.patch('/user/{user_id}', response_model=UserResponse)
async def api_update_user(
    user_id: int,
    data: UpdateUserRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_ownership_user)
):
    return await update_user_service(db, user_id, data, current_user)

# Удаление пользователя (только авторизованный владелец или админ)
@app.delete('/user/{user_id}')
async def api_delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_ownership_user)
):
    return await delete_user_service(db, user_id, current_user)

# РОУТЫ ОБЪЯВЛЕНИЙ (С ДОРАБОТКАМИ ПРАВ)

# Добавлена проверка require_auth для создания
@app.post('/advertisement', response_model=CreateAdvertResponse)
async def api_create_advert(
    data: CreateAdvertRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_auth) # Только авторизованные
):
    try:
        new_advert = await create_advert(db, data, current_user)
        return CreateAdvertResponse(id=new_advert.id)
    except HTTPException as e:
        if e.status_code == 409:
            raise HTTPException(status_code=409, detail="Объявление с такими данными уже существует.")
        raise

# ДОРАБОТКА: Получение доступно всем (зависимость не требуется)
@app.get('/advertisement/{advert_id}', response_model=AdvertResponse)
async def api_get_advert(
    advert_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await get_advert_by_id(db, advert_id)

# ДОРАБОТКА: Добавлена проверка require_ownership_advert
@app.patch('/advertisement/{advert_id}', response_model=AdvertResponse)
async def api_patch_advert(
    advert_id: int,
    data: UpdateAdvertRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_ownership_advert)
):
    return await patch_advert(db, advert_id, data, current_user)

# ДОРАБОТКА: Добавлена проверка require_ownership_advert
@app.delete('/advertisement/{advert_id}')
async def api_delete_advert(
    advert_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_ownership_advert)
):
    await delete_advert(db, advert_id, current_user)
    return {"status": "ok"}

# ДОРАБОТКА: Поиск доступен всем 
@app.get('/advertisement', response_model=list[AdvertResponse])
async def api_search_adverts(
    title: str | None = None,
    author: str | None = None,
    price_min: float | None = None,
    price_max: float | None = None,
    description: str | None = None,
    created_at: str | None = None,
    db: AsyncSession = Depends(get_db)
):
    adverts = await search_adverts(db, title, author, price_min, price_max, description, created_at)
    return adverts