from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import User
from app.dao.general_dao import GeneralDao

class UserDao(GeneralDao[User]):
    _class_type = User

    async def get_by_email(self, email: str, session: AsyncSession) -> User:
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return user
