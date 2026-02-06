from influxdb_client import InfluxDBClient

client = InfluxDBClient(
    url=INFLUXDB_URL,
    token=INFLUXDB_TOKEN,
    org=INFLUXDB_ORG
)

write_api = client.write_api()
query_api = client.query_api()
