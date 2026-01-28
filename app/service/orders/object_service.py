from sqlalchemy.ext.asyncio import AsyncSession
from app.service.general_service import GeneralService
from app.dao import object_dao
from app.db.database import Object
from app.schemas.object import CreateObject, UpdateObject
from app.core.security import hash_password


class ObjectService(GeneralService):
    _class_type = Object
    _dao = object_dao
    _create_schema = CreateObject
    _update_schema = UpdateObject

    async def create(self, data: self._create_schema, session: AsyncSession) -> seld._class_type:
        hash = hash_password(data.password)

        new_obj = self._class_type(
            name=data.name,
            password_hash=hash,
            user_id=data.user_id,
        )

        result = await self._dao.create(new_obj)
        return result

    async def update(self, id: int, data: self._update_schema, session: AsyncSession) -> self._class_type:
        obj = await self._dao.update(id, data)
        data_for_update = data.model_dump(exclude_unset=True)

        if "name" in data_for_update:
            obj.name = data_for_update["name"]

        if "password" in data_for_update:
            obj.password_hash = hash_password(data_for_update["password"])

        if "user_id" in data_for_update:
            obj.user_id = data_for_update["user_id"]

        return obj
