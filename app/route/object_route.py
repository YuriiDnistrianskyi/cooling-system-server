from fastapi import APIRouter, Depends, WebSocket, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from influxdb_client import Point
import json
from datetime import datetime

from app.db.dependencies import get_async_session
from app.db.influxdb import write_api
from app.service import object_service
from app.schemas.object import CreateObject, UpdateObject
from app.core.security import verify_password
from app.ws import ws_manager

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

@object_router.websocket('/ws')
async def object_websocket(
        websocket: WebSocket,
        session: AsyncSession = Depends(get_async_session)
):
    object_id = websocket.query_params.get('object_id')
    password = websocket.query_params.get('password')
    object = await object_service.get_by_id(object_id, session)
    password_is_ok = verify_password(password, object.password_hash)
    if not password_is_ok:
        raise HTTPException(status_code=400, detail="Incorrect password")

    await ws_manager.connect("object", object_id, websocket)

    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            await object_service.write_temperature(object, payload)

    except:
        await ws_manager.disconnect("object", object_id, websocket)
