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
    object_id: int


@device_router.get('/')
async def device_get(session: AsyncSession = Depends(get_async_session)):
    stmt = select(Device)
    devices = await session.execute(stmt)
    result = devices.scalars().all()
    return {'devices': [user.get_info() for user in result]}

@device_router.post('/')
async def device_post(
        data: CreateDevice,
        session: AsyncSession = Depends(get_async_session)):
    data_for_create = {
        'name': data.name,
        'object_id': data.object_id,
        'password_hash': Device.generate_password(data.password)
    }

    new_device = Device.create_device(data_for_create)
    session.add(new_device)
    await session.commit()
    return {'message': 'Device created successfully!'}

