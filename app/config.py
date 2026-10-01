#app/config.py
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "advertisement_db")
    # POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost") # если запускаем НЕ через Docker
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres") # если запускаем через Docker
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    
    DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    # Срок действия токена 24 часа (в секундах)
    TOKEN_TTL = 60 * 60 * 24

config = Config()