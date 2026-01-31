from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Integer, ForeignKey
from typing import Dict
from app.db.database import Base
from app.db.models.object import Object

class Device(Base):
    __tablename__ = "device"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True) #TODO id
    name: Mapped[str] = mapped_column(String)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    object_id: Mapped[int] = mapped_column(Integer, ForeignKey('object.id'))

    # object: Object = relationship('Object', back_populates="devices")

    def get_info(self) -> Dict:
        return {
            'id': self.id,
            'name' : self.name,
            "object_id" : self.object_id
        }

    @staticmethod
    def create_device(data: dict):
        return Device(**data)
