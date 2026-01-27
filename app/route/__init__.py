from fastapi import FastAPI
from .user_route import user_router
from .object_route import object_router
from .device_route import device_router

def connect_router(app: FastAPI) -> None:
    app.include_router(user_router, prefix="/user", tags=["user"])
    app.include_router(object_router, prefix="/object", tags=["object"])
    app.include_router(device_router, prefix="/device", tags=["device"])
