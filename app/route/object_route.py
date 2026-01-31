from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_async_session
from app.service import object_service
from app.schemas.object import CreateObject, UpdateObject

object_router = APIRouter()

@object_router.get('/')
async def object_get(session: AsyncSession = Depends(get_async_session)):
    objects = await object_service.get(session)
    return {'objects': [object.get_info() for object in objects]}

@object_router.post('/')
async def object_post(
        data: CreateObject,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        new_object = await object_service.create(data, session)
        await session.commit()
        await session.refresh(new_object)
        return {"object": new_object.get_info()}
    except:
        await session.rollback()
        raise

@object_router.patch('/{object_id}')
async def object_patch(
        object_id: int,
        data: UpdateObject,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        new_object = await object_service.update(object_id, data, session)
        await session.commit()
        await session.refresh(new_object)
        return {"object": new_object.get_info()}
    except:
        await session.rollback()
        raise

@object_router.delete('/{object_id}')
async def object_delete(
        object_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        await object_service.delete(object_id, session)
        await session.commit()
        return {"message": "Object deleted"}
    except:
        await session.rollback()
        raise
