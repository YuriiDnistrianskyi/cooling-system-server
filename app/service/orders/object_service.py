from sqlalchemy.ext.asyncio import AsyncSession
from influxdb_client import Point
from typing import Dict
from datetime import datetime

from app.service.general_service import GeneralService
from app.dao import object_dao, device_dao
from app.db.database import Object
from app.schemas.object import CreateObject, UpdateObject
from app.core.security import hash_password
from app.core.cooldown import can_send_command
from app.ws import ws_manager


class ObjectService(GeneralService[Object, CreateObject, UpdateObject]):
    _dao = object_dao

    async def get_by_user_id(self, user_id: int, session: AsyncSession) -> list[Object]:
        return await self._dao.get_by_user_id(user_id, session)

    async def get_by_private_name(self, private_name: str, session: AsyncSession) -> Object:
        obj = await self._dao.get_by_private_name(private_name, session)
        if obj is None:
            raise HTTPException(status_code=404, detail='Object private name not found')
        return obj

    async def exists(self, private_name: str, session: AsyncSession) -> bool:
        obj = await self._dao.get_by_private_name(private_name, session)
        if obj is None:
            return False
        return True

    async def create(self, data: CreateObject, session: AsyncSession) -> Object:
        hash = hash_password(data.password)

        new_obj = Object(
            public_name=data.publicName,
            private_name=data.privateName,
            password_hash=hash,
            user_id=data.userId,
            max_temperature=data.maxTemperature,
            default_speed_for_devices=data.defaultSpeedForDevices,
        )

        result = await self._dao.create(new_obj, session)
        return result

    async def update(self, id: int, data: CreateObject,session: AsyncSession) -> Object:
        obj = await self._dao.update(id, session)
        data_for_update = data.model_dump(exclude_unset=True)

        if "publicName" in data_for_update:
            obj.public_name = data_for_update["publicName"]

        if "privateName" in data_for_update:
            obj.private_name = data_for_update["privateName"]

        if "password" in data_for_update:
            obj.password_hash = hash_password(data_for_update["password"])

        if "userId" in data_for_update:
            obj.user_id = data_for_update["userId"]

        if "maxTemperature" in data_for_update:
            obj.max_temperature = data_for_update["maxTemperature"]

        if "defaultSpeedForDevices" in data_for_update:
            obj.default_speed_for_devices = data_for_update["defaultSpeedForDevices"]

        return obj

    async def get_graph(self, object_id: int):
        return None
        #TODO

    async def write_temperature(self, object_id: int, payload: Dict, session: AsyncSession) -> None:
        temperature: float = payload["value"]
        point = (
            Point("temperature")
            .tag("object_id", object_id)
            .field("value", temperature)
            .time(datetime.utcnow())
        )
        await self._dao.write_temperature(point)

        can_send: bool = await can_send_command(object_id)
        first_device: int = await device_dao.get_first_device_by_object_id(object_id, session)
        device_speed: float = await device_dao.get_speed(first_device.id)
        object: Object = await object_dao.get_by_id(object_id, session)

        if temperature > object.max_temperature and can_send:
            payload: dict = {"command": "up"}
            for device in object.devices:
                await ws_manager.send_to("device", device.id, payload)

        elif (temperature < object.max_temperature) and (device_speed > object.default_speed_for_devices) and can_send:
            payload: dict = {"command": "down"}
            for device in object.devices:
                await ws_manager.send_to("device", device.id, payload)
