from influxdb_client import Point

from app.db.database import Device
from app.db.influxdb import write_api, query_api
from app.dao.general_dao import GeneralDao
from app.config import INFLUXDB_BUCKET

class DeviceDao(GeneralDao[Device]):
    _class_type = Device

    async def get_speed(self, device_id: int) -> float:
        query = f"""
                from(bucket: "{INFLUXDB_BUCKET}")
                |> range(start: -30d
                |> filter(fn: (r) => 
                   r._measurement == "speed" and
                   r.device_id == {device_id}
                )
                |> last()
                """
        device_speed: float = query_api.query(query)
        return device_speed

    async def write_speed(self, point: Point) -> None:
        write_api.write(
            bucket=INFLUXDB_BUCKET,
            record=point
        )
