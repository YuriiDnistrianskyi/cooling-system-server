from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
from app.db.database import Base

class Device(Base):
    __tablename__ = "Device"

    device_id: Mapped[str] = mapped_column(String, primary_key=True, autoincrement=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)

    @password.setter
    def password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
