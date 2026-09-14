import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Character(Base):
    __tablename__ = 'characters'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    birth_year = Column(String)
    eye_color = Column(String)
    gender = Column(String)
    hair_color = Column(String)
    homeworld = Column(String)
    mass = Column(String)
    skin_color = Column(String)

async def run_migration():
    DATABASE_URL = "postgresql+asyncpg://postgres:308@localhost:5432/swapi_db"
    
    engine = create_async_engine(DATABASE_URL, echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    print("Миграция завершена: таблица 'characters' создана в PostgreSQL.")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(run_migration())