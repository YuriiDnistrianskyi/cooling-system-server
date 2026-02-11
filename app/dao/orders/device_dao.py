from influxdb_client import Point
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import Device
from app.db.influxdb import write_api, query_api
from app.dao.general_dao import GeneralDao
from app.config import INFLUXDB_BUCKET

class DeviceDao(GeneralDao[Device]):
    _class_type = Device

    async def get_devices_by_object_id(self, object_id: int, session: AsyncSession) -> List[Device]:
        stmt = (
            select(Device)
            .where(Device.object_id == object_id)
        )
        result = await session.execute(stmt)
        devices = result.scalars().all()
        return devices

    async def get_first_device_by_object_id(self, object_id: int, session: AsyncSession) -> List[Device]:
        stmt = (
            select(Device)
            .where(Device.object_id == object_id)
            .limit(1)
        )
        result = await session.execute(stmt)
        device = result.scalars().first()
        return device

    async def get_speed(self, device_id: int) -> float:
        query = f"""
                from(bucket: "{INFLUXDB_BUCKET}")
                |> range(start: -30d)
                |> filter(fn: (r) => 
                   r._measurement == "speed" and
                   r.device_id == "{device_id}"
                )
                |> last()
                """

        tables = query_api.query(query)

        if not tables:
            return 0 # 100

        for table in tables:
            for record in table.records:
                return record.get_value

        return None

    async def write_speed(self, point: Point) -> None:
        write_api.write(
            bucket=INFLUXDB_BUCKET,
            record=point
        )
