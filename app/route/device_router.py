from fastapi import APIRouter
from app.db.database import async_session
from app.db.models.device import Device

device_router = APIRouter()

@device_router.get('/')
async def device_get():
    async with async_session() as session:
        devices = await session.execute(Device).scalars().all()
        return {'devices': devices}

@device_router.post('/')
def device_post():
    pass
