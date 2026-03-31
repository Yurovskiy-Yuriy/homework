"""
Задание 3: Заполнение БД тестовыми данными из JSON-файла
Скрипт читает данные из fixtures/tests_data.json и сохраняет их в базу данных
"""

import json
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker

# Импортируем наши модели и функцию создания таблиц
from book_shop_db import Publisher, Shop, Book, Stock, Sale, Base

DSN = "postgresql://postgres:308@localhost:5432/book_shop_db"

engine = sq.create_engine(DSN)

Session = sessionmaker(bind=engine)

session = Session()

def create_tables_if_not_exists():
    """
    Создает таблицы в БД, если они еще не существуют
    """
    print("Проверка наличия таблиц в БД...")
    Base.metadata.create_all(engine)
    print("Таблицы созданы (если не существовали)")

def clear_tables():
    """
    Очищает таблицы перед загрузкой данных
    (чтобы избежать дублирования при повторном запуске)
    """
    print("Очистка существующих данных...")
    # Удаляем данные в правильном порядке (сначала дочерние, потом родительские)
    session.query(Sale).delete()
    session.query(Stock).delete()
    session.query(Book).delete()
    session.query(Shop).delete()
    session.query(Publisher).delete()
    session.commit()
    print("Данные очищены")

def load_data_from_json(json_file_path):
    """
    Загружает данные из JSON-файла в базу данных
    
    Args:
        json_file_path (str): путь к JSON-файлу с тестовыми данными
    """
    # Открываем и читаем JSON-файл
    with open(json_file_path, 'r', encoding='utf-8') as fd:
        data = json.load(fd)
    
    print(f"Загружено записей из JSON: {len(data)}")
    
    # Создаем словарь соответствия имени модели из JSON и класса модели
    model_mapping = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale
    }
    
    # Счетчики для статистики
    counters = {
        'publisher': 0,
        'shop': 0,
        'book': 0,
        'stock': 0,
        'sale': 0
    }
    
    # Проходим по каждой записи из JSON
    for record in data:
        # Получаем имя модели из JSON
        model_name = record.get('model')
        
        # Получаем соответствующий класс модели
        model_class = model_mapping.get(model_name)
        
        if not model_class:
            print(f"Предупреждение: неизвестная модель '{model_name}', пропускаем")
            continue
        
        # Получаем id и поля из записи
        record_id = record.get('pk')
        fields = record.get('fields', {})
        
        # Проверяем, существует ли уже запись с таким id
        existing = session.query(model_class).filter(model_class.id == record_id).first()
        
        if existing:
            # Если запись существует, обновляем ее
            for key, value in fields.items():
                setattr(existing, key, value)
            print(f"Обновлена {model_name} с id={record_id}")
        else:
            # Создаем новый экземпляр модели
            instance = model_class(id=record_id, **fields)
            session.add(instance)
            print(f"Добавлена {model_name} с id={record_id}")
        
        counters[model_name] += 1
    
    # Сохраняем все изменения в базе данных
    session.commit()
    
    # Выводим статистику
    print("\n" + "="*50)
    print("СТАТИСТИКА ЗАГРУЗКИ:")
    print("="*50)
    for model_name, count in counters.items():
        print(f"{model_name}: {count} записей")
    print("="*50)

def verify_data():
    """
    Проверяет, что данные загружены корректно
    Выводит количество записей в каждой таблице
    """
    print("\nПРОВЕРКА ЗАГРУЖЕННЫХ ДАННЫХ:")
    print("-"*50)
    
    publisher_count = session.query(Publisher).count()
    print(f"Издателей: {publisher_count}")
    
    shop_count = session.query(Shop).count()
    print(f"Магазинов: {shop_count}")
    
    book_count = session.query(Book).count()
    print(f"Книг: {book_count}")
    
    stock_count = session.query(Stock).count()
    print(f"Записей на складе: {stock_count}")
    
    sale_count = session.query(Sale).count()
    print(f"Продаж: {sale_count}")
    
    print("-"*50)
    
    # Если есть данные, показываем пример
    if publisher_count > 0:
        first_publisher = session.query(Publisher).first()
        print(f"Пример издателя: {first_publisher.name}")
    
    if book_count > 0:
        first_book = session.query(Book).first()
        print(f"Пример книги: {first_book.title}")
    
    if shop_count > 0:
        first_shop = session.query(Shop).first()
        print(f"Пример магазина: {first_shop.name}")

def main():
    """
    Основная функция скрипта
    """
    print("="*60)
    print("ЗАГРУЗКА ТЕСТОВЫХ ДАННЫХ В БАЗУ ДАННЫХ")
    print("="*60)
    
    try:
        # Шаг 1: Создаем таблицы (если их нет)
        create_tables_if_not_exists()
        
        # Шаг 2: Очищаем существующие данные
        clear_tables()
        
        # Шаг 3: Загружаем данные из JSON
        json_file = 'fixtures/tests_data.json'
        load_data_from_json(json_file)
        
        # Шаг 4: Проверяем загруженные данные
        verify_data()
        
        print("\n Данные успешно загружены!")
        
    except FileNotFoundError:
        print(f"\n Ошибка: Файл 'fixtures/tests_data.json' не найден!")
        print("Убедитесь, что файл существует и находится в папке fixtures/")
        
    except Exception as e:
        print(f"\n Произошла ошибка: {e}")
        session.rollback()
        
    finally:
        # Закрываем сессию
        session.close()
        print("\nСоединение с БД закрыто")

if __name__ == "__main__":
    main()