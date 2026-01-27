from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Dict
from app.db.database import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    firstName: Mapped[str] = mapped_column(String)
    lastName: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    password_hash: Mapped[str] = mapped_column(String)

    @staticmethod
    def generate_password(password: str) -> None:
        return generate_password_hash(password)

    def check_password(self, password: str) -> Boolean:
        return check_password_hash(self.password_hash, password)

    def get_info(self) -> Dict:
        return {
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email,
        }

    @staticmethod
    def create_user(data: dict):
        return User(**data)
