"""
Задание 2: Запрос выборки магазинов, продающих целевого издателя
Скрипт подключается к БД, принимает имя или ID издателя и выводит все продажи его книг
"""

import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker

# Импортируем наши модели из файла models.py
# Модели нужны чтобы:
#     -Знать, как преобразовывать таблицы в Python-объекты
#     -Понимать связи между таблицами для JOIN
#     -Проверять типы данных
from book_shop_db import Publisher, Book, Stock, Sale, Shop

DSN = "postgresql://postgres:308@localhost:5432/book_shop_db"

engine = sq.create_engine(DSN) # Создаем engine для подключения к БД

Session = sessionmaker(bind=engine) # Создаем фабрику сессий

session = Session() # Создаем сессию — это наш "рабочий стол" для работы с БД

try:
    # ШАГ 1: Ввод данных от пользователя
    print("Введите имя или ID издателя:")
    publisher_input = input().strip()  # strip() удаляет лишние пробелы
    
    # ШАГ 2: Определяем, что ввел пользователь (ID или имя)
    if publisher_input.isdigit():
        publisher_id = int(publisher_input)
        # Ищем издателя по ID
        publisher = session.query(Publisher).filter(Publisher.id == publisher_id).first()
        if not publisher:
            print(f"Издатель с ID {publisher_id} не найден")
            exit()
        print(f"\nНайден издатель: {publisher.name} (ID: {publisher.id})")
    else:
        publisher_name = publisher_input
        # Ищем издателя по имени
        publisher = session.query(Publisher).filter(Publisher.name == publisher_name).first()
        if not publisher:
            print(f"Издатель с именем '{publisher_name}' не найден")
            exit()
        print(f"\nНайден издатель: {publisher.name} (ID: {publisher.id})")
    
    # ШАГ 3: Формируем сложный запрос с JOIN для получения данных о продажах
    # Объяснение JOIN-цепочки:
    # 1. Начинаем с Book, соединяем с Publisher (книга принадлежит издателю)
    # 2. Соединяем со Stock (книга есть на складе)
    # 3. Соединяем с Sale (продажи со склада)
    # 4. Соединяем с Shop (магазин, где находится склад)
    # В итоге получаем все продажи книг нужного издателя
    sales_data = (session.query(
            Book.title,           # название книги
            Shop.name,            # название магазина
            Sale.price,           # цена продажи
            Sale.date_sale        # дата продажи
        )
        .join(Publisher, Book.publisher)           # Book -> Publisher
        .join(Stock, Book.stock)                   # Book -> Stock (через связь stock в Book)
        .join(Sale, Stock.sale)                    # Stock -> Sale (через связь sale в Stock)
        .join(Shop, Stock.shop)                    # Stock -> Shop (через связь shop в Stock)
        .filter(Publisher.id == publisher.id)      # Фильтруем по нашему издателю
        .order_by(Sale.date_sale.desc())           # Сортируем по дате (сначала новые)
        .all()                                      # Получаем все результаты
    )
    
    # ШАГ 4: Проверяем, есть ли результаты
    if not sales_data:
        print(f"\nНет данных о продажах книг издателя '{publisher.name}'")
    else:
        # ШАГ 5: Выводим результаты в требуемом формате
        print("\nРезультаты продаж:")
        print("-" * 70)
        # Форматируем вывод: название книги | магазин | цена | дата
        for book_title, shop_name, price, sale_date in sales_data:
            # Форматируем дату в нужный формат (день-месяц-год)
            formatted_date = sale_date.strftime("%d-%m-%Y")
            # Выводим строку с разделителями |
            print(f"{book_title} | {shop_name} | {price} | {formatted_date}")
        print("-" * 70)
        print(f"Всего найдено записей: {len(sales_data)}")
        
except Exception as e:
    print(f"Произошла ошибка: {e}")
    # Если нужно, можно сделать rollback, но в данном случае это select, поэтому не обязательно
    # session.rollback()
    
finally:
    # ШАГ 6: Закрываем сессию 
    session.close()