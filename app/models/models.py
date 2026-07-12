from app.database.database import Base

from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime

class Watcher(Base):
    __tablename__ = 'watchers'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    
    name: Mapped[str] = mapped_column(String(100))
    source_type: Mapped[str] = mapped_column(String(50))
    product_id: Mapped[str]
    cc: Mapped[str] = mapped_column(String(10), default='vn')
    
    target_price: Mapped[str]
    interval_minutes: Mapped[int] = mapped_column(Integer, default=30)
    notify_to: Mapped[str] = mapped_column(String(10))
    
    last_state: Mapped[bool] = mapped_column(Boolean, default=False)
    last_price: Mapped[int] = mapped_column(Integer, nullable=True)
    last_checked_at: Mapped[datetime]
    
    user: Mapped['User'] = relationship(back_populates='watchers')

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str]
    hashed_password: Mapped[str]
    
    watchers: Mapped[list[Watcher]] = relationship(back_populates='user')