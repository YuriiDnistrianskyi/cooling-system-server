from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from typing import List, Dict
from app.db.database import Base

class Object(Base):
    __tablename__ = 'object'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    public_name: Mapped[str] = mapped_column(String)
    private_name: Mapped[str] = mapped_column(String)
    password_hash: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    max_temperature: Mapped[float] = mapped_column(Integer)
    default_speed_for_devices: Mapped[int] = mapped_column(Integer)

    devices: Mapped[List["Device"]] = relationship("Device", back_populates="object")

    # owner: User = relationship("User", back_populates="devices")

    def get_info(self) -> Dict:
        return {
            'id': self.id,
            'public_name': self.public_name,
            'private_name': self.private_name,
            'max_temperature': self.max_temperature,
            'default_speed_for_devices': self.default_speed_for_devices,
            'user_id': self.user_id
        }

    @staticmethod
    def create_object(data: dict):
        return Object(**data)

