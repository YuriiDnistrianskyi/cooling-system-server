from sqlalchemy.ext.asyncio import AsyncSession
from influxdb_client import Point
from detetime import datetime

from app.service.general_service import GeneralService
from app.dao import device_dao
from app.db.database import Device
from app.schemas.device import CreateDevice, UpdateDevice
from app.core.security import hash_password


class DeviceService(GeneralService[Device, CreateDevice, UpdateDevice]):
    _dao = device_dao

    async def create(self, data: CreateDevice, session: AsyncSession) -> Device:
        hash = hash_password(data.password)

        new_obj = Device(
            name=data.name,
            password_hash=hash,
            object_id=data.object_id,
        )

        result = await self._dao.create(new_obj, session)
        return result

    async def update(self, id: int, data: UpdateDevice, session: AsyncSession) -> Device:
        obj = await self._dao.update(id, session)
        data_for_update = data.model_dump(exclude_unset=True)

        if "name" in data_for_update:
            obj.name = data_for_update["name"]

        if "password" in data_for_update:
            obj.password_hash = hash_password(data_for_update["password"])

        if "object_id" in data_for_update:
            obj.object_id = data_for_update["object_id"]

        return obj

    async def write_speed(self, device_id: int, payload: dict) -> None:
        speed: int = payload["value"]
        point: Point = Point(
            Point("speed")
            .tag("device_id", device_id)
            .field("value", speed)
            .time(datetime.utcnow())
        )

        await self._dao.write_speed(point)

