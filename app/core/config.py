from os import getenv
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = getenv("DATABASE_URL")
INFLUXDB_URL = getenv("INFLUXDB_URL")
INFLUXDB_TOKEN = getenv("INFLUXDB_TOKEN")
INFLUXDB_ORG = getenv("INFLUXDB_ORG")
INFLUXDB_BUCKET = getenv("INFLUXDB_BUCKET")

SECRET_KEY = getenv("SECRET_KEY")

COOLDOWN = int(getenv("COOLDOWN"))
