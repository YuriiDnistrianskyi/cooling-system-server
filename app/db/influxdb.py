from influxdb_client import InfluxDBClient

from app.config import INFLUXDB_URL, INFLUXDB_TOKEN, INFLUXDB_ORG

client = InfluxDBClient(
    url=INFLUXDB_URL,
    token=INFLUXDB_TOKEN,
    org=INFLUXDB_ORG
)

write_api = client.write_api()
query_api = client.query_api()
