from sqlalchemy.ext.asyncio import AsyncSession
from influxdb_client import Point
from typing import Dict

from app.service.general_service import GeneralService
from app.dao import object_dao, device_dao
from app.db.database import Object
from app.db.influxdb import query_api
from app.schemas.object import CreateObject, UpdateObject
from app.core.security import hash_password
from app.core.cooldown import can_send_command
from app.ws import ws_manager
from app.config import INFLUXDB_BUCKET


class ObjectService(GeneralService[Object, CreateObject, UpdateObject]):
    _dao = object_dao

    async def create(self, data: CreateObject, session: AsyncSession) -> Object:
        hash = hash_password(data.password)

        new_obj = Object(
            name=data.name,
            password_hash=hash,
            user_id=data.user_id,
            max_temperature=data.max_temperature,
            default_speed_for_devices=data.default_speed_for_devices,
        )

        result = await self._dao.create(new_obj, session)
        return result

    async def update(self, id: int, data: CreateObject,session: AsyncSession) -> Object:
        obj = await self._dao.update(id, session)
        data_for_update = data.model_dump(exclude_unset=True)

        if "name" in data_for_update:
            obj.name = data_for_update["name"]

        if "password" in data_for_update:
            obj.password_hash = hash_password(data_for_update["password"])

        if "user_id" in data_for_update:
            obj.user_id = data_for_update["user_id"]

        if "max_temperature" in data_for_update:
            obj.max_temperature = data_for_update["max_temperature"]

        if "default_speed_for_devices" in data_for_update:
            obj.default_speed_for_devices = data_for_update["default_speed_for_devices"]

        return obj

    async def write_temperature(self, object: Object, payload: Dict):
        temperature: float = payload["value"]
        point = Point(
            Point("temperature")
            .tag("object_id", object_id)
            .field("value", temperature)
            .time(datetime.utcnow())
        )
        await self._dao.write_temperature(point)

        can_send: bool = await can_send_command(object_id)
        first_device_id: int = object.devices[0].id
        device_speed: float = await device_dao.get_speed(first_device_id)

        if tempeature > object.max_temperature and can_send:
            payload: dict = {"command": "up"}
            for device in object.devices:
                await ws_manager.send_to("device", device.id, payload)

        elif (temperature < object.max_temperature) and (device_speed > object.default_speed_for_devices) and can_send:
            payload: dict = {"command": "down"}
            for device in object.devices:
                await ws_manager.send_to("device", device.id, payload)
