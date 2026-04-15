from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_async_session
from app.core.get_current_user import get_current_user
from app.service import user_service
from app.schemas.user import CreateUser, UpdateUser

user_router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@user_router.get('/')
async def user_get(session: AsyncSession = Depends(get_async_session)):
    users = await user_service.get(session)
    return {'list': [user.get_info() for user in users]}

@user_router.get('/{user_id}')
async def user_get_by_id(
        user_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        user = await user_service.get_by_id(user_id, session)
        return {'obj': user.get_info()}
    except:
        raise

@user_router.post('/')
async def user_post(
        data: CreateUser,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        new_user = await user_service.create(data, session)
        await session.commit()
        await session.refresh(new_user)
        return {"obj": new_user.get_info()}
    except:
        await session.rollback()
        raise

@user_router.patch('/{user_id}')
async def user_patch(
        user_id: int,
        data: UpdateUser,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        new_user = await user_service.update(user_id, data, session)
        await session.commit()
        await session.refresh(new_user)
        return {"obj": new_user.get_info()}
    except:
        await session.rollback()
        raise

@user_router.delete('/{user_id}')
async def user_delete(
        user_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        await user_service.delete(user_id, session)
        await session.commit()
        return {"message": "User deleted"}
    except:
        await session.rollback()
        raise
