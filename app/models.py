#add/models.py
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from datetime import datetime  
from sqlalchemy.sql import func
from sqlalchemy import String, ForeignKey, Uuid, DateTime  
import uuid

Base = declarative_base()

class Role(Base):
    __tablename__ = 'role'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)

class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(100), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey('role.id'), default=1, nullable=False)
    
    role: Mapped["Role"] = relationship(lazy="joined")
    adverts: Mapped[list["Advertisement"]] = relationship(back_populates="author_obj", cascade="all, delete-orphan")

class Token(Base):
    __tablename__ = 'token'
    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[uuid.UUID] = mapped_column(
        Uuid, 
        server_default=func.gen_random_uuid(), 
        unique=True, 
        nullable=False
    )
    # datetime (Python) для Mapped, DateTime (SQLAlchemy) для mapped_column
    creation_time: Mapped[datetime] = mapped_column(
        DateTime, 
        server_default=func.now(), 
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped["User"] = relationship(lazy="joined")

class Advertisement(Base):
    __tablename__ = 'adverts'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(String(500))
    price: Mapped[float] = mapped_column()
    author: Mapped[str] = mapped_column(String(100))
    
    # Поле для связи с пользователем (для проверки прав "свой/чужой")
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=True)
    author_obj: Mapped["User"] = relationship("User", back_populates="adverts", lazy="joined")
    
    # datetime (Python) для Mapped, DateTime (SQLAlchemy) для mapped_column
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    