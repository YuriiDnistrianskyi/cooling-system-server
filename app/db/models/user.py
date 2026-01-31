from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from typing import Dict
from app.db.database import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    password_hash: Mapped[str] = mapped_column(String)

    def get_info(self) -> Dict:
        return {
            'id': self.id,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'email': self.email,
        }

    @staticmethod
    def create_user(data: dict):
        return User(**data)
