from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dependencies import get_async_session
from app.db.models.user import User

user_router = APIRouter()

class CreateUser(BaseModel):
    firstName: str
    lastName: str
    email: str
    password: str


@user_router.get('/')
async def user_get(session: AsyncSession = Depends(get_async_session)):
    stmt = select(User)
    users = await session.execute(stmt)
    result = users.scalars().all()
    return {'users': [user.get_info() for user in result]}


@user_router.post('/')
async def user_post(
        data: CreateUser,
        session: AsyncSession = Depends(get_async_session)
):
    data_for_create = {
        'firstName': data.firstName,
        'lastName': data.lastName,
        'email': data.email,
        'password_hash': User.generate_password(data.password)
    }

    new_user = User.create_user(data_for_create)
    session.add(new_user)
    await session.commit()
    return {'message': 'User created successfully!'}
