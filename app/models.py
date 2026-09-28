#add/models.py
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from datetime import datetime as DateTime
from sqlalchemy.sql import func
Base = declarative_base()

class Advertisement(Base):
    __tablename__ = 'adverts'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[int] = mapped_column()
    author: Mapped[str]
    created_at: Mapped[DateTime] = mapped_column(server_default=func.now())