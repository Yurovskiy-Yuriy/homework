import psycopg2
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()   # Создаём базовый класс для всех моделей

class Publisher(Base):
    __tablename__ = "publisher"   

    id = sq.Column(sq.Integer, primary_key=True)   
    name = sq.Column(sq.String(length=40), nullable=False)  # Автор

    # Связь с книгами (один автор -> много книг)
    book = relationship("Book", back_populates="publisher") 

    def __str__(self):  
        return f'Publisher {self.id}: {self.name}' 

class Book(Base): 
    __tablename__ = "book"  

    id = sq.Column(sq.Integer, primary_key=True)  
    title = sq.Column(sq.String(length=40), nullable=False)  # имя книги

    # Внешний ключ на автора 
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False) #ссылаемся на publisher.id

    # Обратная связь на Cours
    publisher = relationship("Publisher", back_populates="book") # Нужно указывать имя класса в кавычках
    stock = relationship("Stock", back_populates="book")

    def __str__(self): 
        return f'Book {self.id}: {self.title}, (publisher_id={self.id_publisher})'
    
class Shop(Base):
    __tablename__ = "shop"  

    id = sq.Column(sq.Integer, primary_key=True)  
    name = sq.Column(sq.String(length=40), nullable=False) 

    # Связь со складом (один магазин -> много записей на складе)
    stock = relationship("Stock", back_populates="shop")  # связь с таблицами

    def __str__(self):  
        return f'Shop {self.id}: {self.name}' 
class Stock(Base):
    __tablename__ = "stock"   #  имя таблицы в БД

    id = sq.Column(sq.Integer, primary_key=True)   
    count = sq.Column(sq.Integer)  # количество книг в наличии

    # Внешние ключи 
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)

    # Связи
    sale = relationship("Sale", back_populates="stock")  
    book = relationship("Book", back_populates="stock")  
    shop = relationship("Shop", back_populates="stock")  
    

    def __str__(self):  
        return f'Stock {self.id}: count={self.count}, book_id={self.id_book}, shop_id={self.id_shop}'

class Sale(Base):
    __tablename__ = "sale"   

    id = sq.Column(sq.Integer, primary_key=True)   
    price = sq.Column(sq.Integer)  # цена продажи
    date_sale = sq.Column(sq.Date)  # дата продажи
    count = sq.Column(sq.Integer, nullable=False)  # количество проданных книг

    # Внешний ключ на stock
    id_stock= sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)

    # Связь со складом
    stock = relationship("Stock", back_populates="sale") 

   

    def __str__(self):  # чтобы нормально отображались ячейки при print()
        return f'Sale {self.id}: {self.price}, {self.date_sale}, {self.id_stock}, {self.count}' 


# подключаемся к БД и создаем таблицы
DSN = "postgresql://postgres:308@localhost:5432/book_shop_db"
engine = sq.create_engine(DSN)    # создается объект для взаимодействия с БД.
Base.metadata.create_all(engine) 
