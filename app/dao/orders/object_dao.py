from influxdb_client import Point
from typing import Dict

from app.db.database import Object
from app.db.influxdb import write_api
from app.dao.general_dao import GeneralDao
from app.core.config import INFLUXDB_BUCKET, INFLUXDB_ORG

class ObjectDao(GeneralDao[Object]):
    _class_type = Object

    async def write_temperature(self, point: Point) -> None:
        write_api.write(
            bucket=INFLUXDB_BUCKET,
            org=INFLUXDB_ORG,
            record=point
        )
