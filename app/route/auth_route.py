from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.jwt import create_access_token, create_refresh_token, verify_token
from app.core.security import verify_password
from app.db.dependencies import get_async_session
from app.service import user_service
from app.schemas.auth import Login
from app.schemas.user import CreateUser

auth_router = APIRouter()

@auth_router.post('/register')
async def register(
        data: CreateUser,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        user = await user_service.create(data, session)
        await session.commit()
        await session.refresh(user)
        return {'user': user.get_info()}
    except:
        await session.rollback()
        raise

@auth_router.post('/login')
async def login(
        data: Login,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        user = await user_service.get_by_email(data.email, session)
        if not verify_password(data.password, user.password_hash):
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        return {'access_token': access_token, 'refresh_token': refresh_token, 'user_id': user.id}
    except:
        raise

@auth_router.post('/refresh')
async def refresh(
        refresh_token: str
):
    try:
        payload = verify_token(refresh_token)
        user_id = payload['user_id']
        access_token = create_access_token(user_id)
        return {'access_token': access_token}
    except:
        raise
