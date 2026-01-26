from fastapi import FastAPI
from .fan_router import fan_router
from .cpu_router import cpu_router
from .device_router import device_router

def connect_router(app: FastAPI) -> None:
    app.include_router(fan_router, prefix="/fan", tags=["fan"])
    app.include_router(cpu_router, prefix="/cpu", tags=["cpu"])
    app.include_router(device_router, prefix="/device", tags=["device"])
