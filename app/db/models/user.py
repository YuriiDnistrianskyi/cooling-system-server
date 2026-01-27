from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
from app.db.database import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    firstName: Mapped[str] = mapped_column(String)
    lastName: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    password_hash: Mapped[str] = mapped_column(String)

    def generate_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> Boolean:
        return check_password_hash(self.password_hash, password)
