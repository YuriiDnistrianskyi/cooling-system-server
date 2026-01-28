from sqlalchemy.ext.asyncio import AsyncSession
from app.service.general_service import GeneralService
from app.dao import device_dao
from app.db.database import Device
from app.schemas.device import DeviceCreate, DeviceUpdate
from app.core.security import hash_password

class DeviceService(GeneralService):
    _class_type = Device
    _dao = device_dao
    _create_schema = DeviceCreate
    _update_schema = DeviceUpdate

    async def create(self, data: self._create_schema, session: AsyncSession) -> Device:
        hash = hash_password(data.password)

        new_obj = self._class_type(
            name=data.name,
            password_hash=hash,
            object_id=data.object_id,
        )

        result = await self._dao.create(new_obj)
        return result
