from sqlalchemy.ext.asyncio import AsyncSession
from app.service.general_service import GeneralService
from app.dao import user_dao
from app.db.database import User
from app.schemas.user import CreateUser, UpdateUser
from app.core.security import hash_password


class UserService(GeneralService[User, CreateUser, UpdateUser]):
    _dao = user_dao

    async def get_by_email(self, email, session) -> User:
        return await self._dao.get_by_email(email, session)

    async def create(self, data: CreateUser, session: AsyncSession) -> User:
        hash = hash_password(data.password)

        new_obj = User(
            first_name=data.firstName,
            last_name=data.lastName,
            email=data.email,
            password_hash=hash
        )

        result = await self._dao.create(new_obj, session)
        return result

    async def update(self, id: int, data: UpdateUser, session: AsyncSession) -> User:
        obj = await self._dao.update(id, session)
        data_for_update = data.model_dump(exclude_unset=True)

        if "firstName" in data_for_update:
            obj.first_name = data_for_update["firstName"]

        if "lastName" in data_for_update:
            obj.last_name = data_for_update["lastName"]

        if "email" in data_for_update:
            obj.email = data_for_update["email"]

        if "password" in data_for_update:
            obj.password_hash = hash_password(data_for_update["password"])

        return obj
