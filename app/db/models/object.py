from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from typing import List
from app.db.database import Base

class Object(Base):
    __tablename__ = 'object'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    # from app.db.models.device import Device
    # devices = relationship("Device", back_populates="object")

    # owner: User = relationship("User", back_populates="devices")
