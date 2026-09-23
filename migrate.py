import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from models import Base
from config import DATABASE_URL

async def run_migration():
    engine = create_async_engine(DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Миграция завершена: таблица 'ads' создана в PostgreSQL.")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(run_migration())