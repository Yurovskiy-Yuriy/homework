import asyncio
from typing import List, Dict, Any

import httpx
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select

from models import Base, Character, run_migration
from sqlalchemy import text


# --- Константы ---
DATABASE_URL = "postgresql+asyncpg://postgres:308@localhost:5432/swapi_db"
BASE_API_URL = "https://www.swapi.tech/api/people/"
PLANET_API_URL = "https://www.swapi.tech/api/planets/"
BATCH_SIZE = 10

# Задержка между запросами к планетам, чтобы избежать 429 ошибки
PLANET_REQUEST_DELAY = 2 

# --- Создание движка ---
engine = create_async_engine(DATABASE_URL, echo=False)

# Словарь-кэш для названий планет
_planet_cache: Dict[str, str] = {}


async def get_planet_name(client: httpx.AsyncClient, url: str) -> str:
    """
    Получает имя планеты по URL с использованием кэша и задержки.
    """
    if not url or url in _planet_cache:
        return _planet_cache.get(url, "Unknown")
    
    try:
        # Ждем перед каждым новым запросом к планете 
        await asyncio.sleep(PLANET_REQUEST_DELAY)
        
        print(f"[СЕТЬ] Запрашиваем название планеты: {url}")
        response = await client.get(url)
        response.raise_for_status()
        
        data = response.json()
        name = data.get("result", {}).get("properties", {}).get("name")
        
        _planet_cache[url] = name or "Unknown"
        return _planet_cache[url]
    except Exception as e:
        print(f"[ОШИБКА ПЛАНЕТЫ] {url}: {e}")
        _planet_cache[url] = "Unknown"
        return "Unknown"


async def fetch_character(client: httpx.AsyncClient, char_id: int) -> Dict[str, Any] | None:
    try:
        response = await client.get(f"{BASE_API_URL}{char_id}/")
        response.raise_for_status()
        
        data = response.json()
        props = data.get("result", {}).get("properties", {})
        
        if not props:
            return None
            
        planet_name = await get_planet_name(client, props.get("homeworld"))
            
        return {
            "id": int(char_id),
            "name": props.get("name"),
            "birth_year": props.get("birth_year"),
            "eye_color": props.get("eye_color"),
            "gender": props.get("gender"),
            "hair_color": props.get("hair_color"),
            "homeworld": planet_name,
            "mass": props.get("mass"),  
            "skin_color": props.get("skin_color"),
        }
    except (httpx.HTTPStatusError, ValueError, KeyError):
        return None


async def save_characters(session: AsyncSession, characters: List[Dict[str, Any]]):
    """Надежный UPSERT через ON CONFLICT."""
    if not characters:
        return

    dicts_to_insert = []
    for char in characters:
        raw_mass = char.get('mass')
        clean_mass_str = None 
        
        if raw_mass and str(raw_mass).lower() != "unknown":
            mass_str = str(raw_mass).replace(",", "").replace("?", "")
            try:
                # Преобразуем в число
                temp_float = float(mass_str)      
                #  превращаем число обратно в строку.
                if temp_float.is_integer():
                    clean_mass_str = str(int(temp_float))
                else:
                    clean_mass_str = str(temp_float)
                    
            except ValueError:
                clean_mass_str = None
        
        row = {
            "id": int(char['id']),
            "name": char.get('name'),
            "birth_year": char.get('birth_year'),
            "eye_color": char.get('eye_color'),
            "gender": char.get('gender'),
            "hair_color": char.get('hair_color'),
            "homeworld": char.get('homeworld'),
            "mass": clean_mass_str,      
            "skin_color": char.get('skin_color'),
        }
        dicts_to_insert.append(row)
    
    insert_stmt = text("""
        INSERT INTO characters (id, name, birth_year, eye_color, gender, hair_color, homeworld, mass, skin_color)
        VALUES (:id, :name, :birth_year, :eye_color, :gender, :hair_color, :homeworld, :mass, :skin_color)
        ON CONFLICT (id) DO UPDATE SET
            name = EXCLUDED.name,
            birth_year = EXCLUDED.birth_year,
            eye_color = EXCLUDED.eye_color,
            gender = EXCLUDED.gender,
            hair_color = EXCLUDED.hair_color,
            homeworld = EXCLUDED.homeworld,
            mass = EXCLUDED.mass,
            skin_color = EXCLUDED.skin_color;
    """)
    
    try:
        await session.execute(insert_stmt, dicts_to_insert)
        await session.commit()
    except Exception as db_error:
        # Выводим ошибку и откатываем
        print(f"[ОШИБКА БАЗЫ ДАННЫХ] Не удалось сохранить пакет. Откат. Текст: {db_error}")
        await session.rollback()


async def main():
    print("Шаг 1: Проверка и создание таблицы...")
    await run_migration()

    async with httpx.AsyncClient(timeout=30.0) as client:
        print("Шаг 2: Начало загрузки данных...")
        
        tasks = [fetch_character(client, i) for i in range(1, 101)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        valid_results = []
        errors_found = False
        
        for i, res in enumerate(results):
            if isinstance(res, Exception):
                print(f"[ОШИБКА] Задача {i+1} завершилась исключением: {type(res).__name__} - {res}")
                errors_found = True
            elif res is None:
                print(f"[ИНФО] Персонаж с ID {i+1} не найден (None).")
            else:
                valid_results.append(res)
                
        print(f"Загружено {len(valid_results)} валидных профилей из 100 запрошенных.")
        
        if not valid_results:
            print("В БД нечего сохранять, завершаем работу.")
            return

        print("Шаг 3: Сохранение в базу данных...")
        async with AsyncSession(engine) as session:
            try:
                await save_characters(session, valid_results)
                
                result = await session.execute(select(Character))
                loaded_count = len(result.scalars().all())
                print(f"ПРОВЕРКА: После commit() в базе обнаружено {loaded_count} записей.")
                
            except Exception as e:
                print(f"[КРИТИЧНАЯ ОШИБКА СОХРАНЕНИЯ] Тип: {type(e).__name__}")
                print(f"[КРИТИЧНАЯ ОШИБКА СОХРАНЕНИЯ] Текст: {e}")
                await session.rollback()


if __name__ == "__main__":
    asyncio.run(main())