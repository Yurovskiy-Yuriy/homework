import os
from dotenv import load_dotenv

# Загружаем переменные из файла .env
load_dotenv()

# Получаем переменные
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

# Проверка
if not all([DB_USER, DB_PASS, DB_NAME]):
    raise ValueError("Ошибка: Не заданы обязательные переменные DB_USER, DB_PASS или DB_NAME в файле .env")

# Формируем итоговый URL
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"