from influxdb_client import Point
from typing import Dict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import Object
from app.db.influxdb import write_api
from app.dao.general_dao import GeneralDao
from app.core.config import INFLUXDB_BUCKET, INFLUXDB_ORG

class ObjectDao(GeneralDao[Object]):
    _class_type = Object

    async def get_by_user_id(self, user_id: int, session: AsyncSession) -> list[Object]:
        stmt = select(Object).where(Object.user_id == user_id)
        _list = await session.execute(stmt)
        result = _list.scalars().all()
        return result


    async def write_temperature(self, point: Point) -> None:
        write_api.write(
            bucket=INFLUXDB_BUCKET,
            org=INFLUXDB_ORG,
            record=point
        )
