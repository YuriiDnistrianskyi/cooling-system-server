from sqlalchemy.ext.asyncio import AsyncSession
from app.service.general_service import GeneralService
from app.dao import user_dao
from app.db.database import User
from app.schemas.user import CreateUser, UpdateUser
from app.core.security import hash_password


class UserService(GeneralService):
    _class_type = User
    _dao = user_dao
    _create_schema = CreateUser
    _update_schema = UpdateUser

    async def create(self, data: self._create_schema, session: AsyncSession) -> Device:
        hash = hash_password(data.password)

        new_obj = self._class_type(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            password_hash=hash
        )

        result = await self._dao.create(new_obj)
        return result
