from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Integer, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Dict
from app.db.database import Base
from app.db.models.object import Object

class Device(Base):
    __tablename__ = "Device"

    device_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True) #TODO id
    name: Mapped[str] = mapped_column(String)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    object_id: Mapped[int] = mapped_column(Integer, ForeignKey('object.id'))

    # object: Object = relationship('Object', back_populates="devices")

    @staticmethod
    def generate_password(password: str) -> str:
        password_hash = generate_password_hash(password)
        return password_hash

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def get_info(self) -> Dict:
        return {
            'id': self.device_id,
            'name' : self.name,
            "object_id" : self.object_id
        }

    @staticmethod
    def create_device(data: dict):
        return Device(**data)
