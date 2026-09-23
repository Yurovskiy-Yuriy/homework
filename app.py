import os
from aiohttp import web
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from datetime import datetime, timezone
from dotenv import load_dotenv

from models import Base, Ad
from config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=False)

# --- Сессия на каждый запрос ---
async def get_session():
    async with AsyncSession(engine) as session:
        yield session

# --- Вспомогательные функции ---
async def get_ad_or_404(session: AsyncSession, ad_id: int):
    result = await session.execute(select(Ad).where(Ad.id == ad_id))
    ad = result.scalar_one_or_none()
    if not ad:
        raise web.HTTPNotFound(
            text='{"error": "Объявление не найдено"}',
            content_type="application/json"
        )
    return ad

# --- View-функции ---
async def hello(request):
    return web.json_response({"message": "Aiohttp + SQLAlchemy + PostgreSQL готов!"})

async def get_ads(request):
    async with AsyncSession(engine) as session:
        result = await session.execute(select(Ad).order_by(Ad.id.desc()))
        ads = result.scalars().all()
    return web.json_response([ad.to_dict() for ad in ads])

async def create_ad(request):
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"error": "Тело запроса должно быть JSON"}, status=400)

    title = data.get("title")
    description = data.get("description")
    owner = data.get("owner")

    if not all([title, description, owner]):
        return web.json_response(
            {"error": "Обязательные поля: title, description, owner"},
            status=400
        )

    async with AsyncSession(engine) as session:
        new_ad = Ad(
            title=title,
            description=description,
            owner=owner,
            created_at=datetime.now(timezone.utc)
        )
        session.add(new_ad)
        await session.commit()
        await session.refresh(new_ad)

    return web.json_response(new_ad.to_dict(), status=201)

async def get_ad(request):
    ad_id = int(request.match_info['ad_id'])
    async with AsyncSession(engine) as session:
        ad = await get_ad_or_404(session, ad_id)
    return web.json_response(ad.to_dict())

async def update_ad(request):
    ad_id = int(request.match_info['ad_id'])

    try:
        data = await request.json()
    except Exception:
        return web.json_response(
            {"error": "Тело запроса должно быть валидным JSON"},
            status=400
        )

    async with AsyncSession(engine) as session:
        ad = await get_ad_or_404(session, ad_id)

        if "title" in data:
            ad.title = data["title"]
        if "description" in data:
            ad.description = data["description"]
        if "owner" in data:
            ad.owner = data["owner"]

        await session.commit()
        await session.refresh(ad)

    return web.json_response(ad.to_dict())

async def delete_ad(request):
    ad_id = int(request.match_info['ad_id'])

    async with AsyncSession(engine) as session:
        ad = await session.get(Ad, ad_id)
        if not ad:
            return web.json_response(
                {"error": "Объявление не найдено"},
                status=404
            )
        await session.delete(ad)
        await session.commit()

    return web.json_response({"message": "Объявление удалено"})

# --- Приложение ---
def init_app():
    app = web.Application()

    app.router.add_get(r'/', hello)
    app.router.add_get(r'/ads', get_ads)
    app.router.add_post(r'/ads', create_ad)
    app.router.add_get(r'/ads/{ad_id:\d+}', get_ad)
    app.router.add_put(r'/ads/{ad_id:\d+}', update_ad)
    app.router.add_delete(r'/ads/{ad_id:\d+}', delete_ad)

    return app

if __name__ == '__main__':
    web.run_app(init_app(), host='0.0.0.0', port=8080)