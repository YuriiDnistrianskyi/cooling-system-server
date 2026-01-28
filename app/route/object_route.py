from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_async_session
from app.db.models.object import Object

object_router = APIRouter()

class CreateObject(BaseModel):
    name: str
    user_id: int

@object_router.get('/')
async def object_get(session: AsyncSession = Depends(get_async_session)):
    stmt = select(Object)
    objects = await session.execute(stmt)
    result = objects.scalars().all()
    return {'objects': [object.get_info() for object in result]}

@object_router.post('/')
async def object_post(
        data: CreateObject,
        session: AsyncSession = Depends(get_async_session)
):
    data_for_create = {
        'name': data.name,
        'user_id': data.user_id
    }

    new_object = Object.create_object(data_for_create)
    session.add(new_object)
    await session.commit()
    return {'message': 'Object created successfully!'}

@object_router.delete('/{object_id}')
async def device_delete(
        object_id: int,
        session: AsyncSession = Depends(get_async_session)):
    device = await session.get(Object, object_id)
    if not device:
        return {'message': 'Device not found!'}

    await session.delete(device)
    await session.commit()

    return {'message': 'Device deleted successfully!'}
