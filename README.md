# Cooling System Backend

Backend service for the Cooling System project.

The server is responsible for:

* User authentication and authorization
* Device management
* Object management
* WebSocket communication
* Temperature processing
* Cooling control logic
* Data storage

## Technologies

* Python
* FastAPI
* SQLAlchemy
* Alembic
* PostgreSQL
* InfluxDB
* WebSocket

## Databases

### PostgreSQL

Stores metadata:

* Users
* Devices
* Objects

### InfluxDB

Stores telemetry data:

* Temperature measurements
* Fan RPM measurements

## WebSocket Communication

The backend communicates with:

* Monitoring scripts (temperature sources)
* ESP8266 cooling devices

## Cooling Workflow

1. Client sends temperature data.
2. Backend processes incoming measurements.
3. Cooling algorithm determines the required fan speed.
4. Command is sent to the corresponding device.
5. Device adjusts PWM output.
6. RPM and temperature data are stored in InfluxDB.

## Installation

```bash
git clone https://github.com/YuriiDnistrianskyi/cooling-system-server
cd app

python -m venv .venv

source .venv/bin/activate
# Windows
# .venv\Scripts\activate

pip install -r requirements.txt
```

## Database Migration

```bash
alembic upgrade head
```

## Run

```bash
uvicorn app.main:app --reload
```

## Features

* REST API
* WebSocket support
* Device authentication
* Object authentication
* PostgreSQL integration
* InfluxDB integration
* Automatic cooling control
* Historical telemetry storage

```
```
