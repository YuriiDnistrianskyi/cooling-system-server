from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_async_session
from app.db.models.device import Device

device_router = APIRouter()

class CreateDevice(BaseModel):
    name: str
    password: str
    object_id:


@device_router.get('/')
async def device_get(session: AsyncSession = Depends(get_async_session)):
    stmt = select(Device)
    devices = await session.execute(stmt)
    result = devices.scalars().all()
    return {"devices": result}

@device_router.post('/')
def device_post(
        session: AsyncSession = Depends(get_async_session),
        data: CreateDevice
                ):

    pass
