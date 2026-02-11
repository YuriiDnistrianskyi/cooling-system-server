from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
import json

from app.db.dependencies import get_async_session
from app.service import device_service
from app.schemas.device import CreateDevice, UpdateDevice
from app.ws import ws_manager
from app.core.security import verify_password

device_router = APIRouter()

@device_router.get('/')
async def device_get(session: AsyncSession = Depends(get_async_session)):
    devices = await device_service.get(session)
    return {'devices': [device.get_info() for device in devices]}

@device_router.post('/')
async def device_post(
        data: CreateDevice,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        new_device = await device_service.create(data, session)
        await session.commit()
        await session.refresh(new_device)
        return {"device": new_device.get_info()}
    except:
        await session.rollback()
        raise

@device_router.patch('/{device_id}')
async def device_patch(
        device_id: int,
        data: UpdateDevice,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        new_device = await device_service.update(device_id, data, session)
        await session.commit()
        await session.refresh(new_device)
        return {"device": new_device.get_info()}
    except:
        await session.rollback()
        raise

@device_router.delete('/{device_id}')
async def device_delete(
        device_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        await device_service.delete(device_id, session)
        await session.commit()
        return {"message": "Device deleted"}
    except:
        await session.rollback()
        raise

@device_router.websocket('/ws')
async def device_websocket(
        websocket: WebSocket,
        session: AsyncSession = Depends(get_async_session)
):
    device_id = int(websocket.query_params.get('device_id'))
    password = websocket.query_params.get('password')
    device = await device_service.get_by_id(device_id, session)
    password_is_ok = verify_password(password, device.password_hash)
    if not password_is_ok:
        raise HTTPException(status_code=400, detail="Incorrect password")

    await ws_manager.connect("device", device_id, websocket)

    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            await device_service.write_speed(device_id, payload)

    except:
        await ws_manager.disconnect("device", device_id, websocket)
