from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Generic, TypeVar, List

T = TypeVar("T")
CreateSchema = TypeVar("CreateSchema")
UpdateSchema = TypeVar("UpdateSchema")

class GeneralService(Generic[T, CreateSchema, UpdateSchema]):
    _dao = None

    async def get(self, session: AsyncSession) -> List[T]:
        list = await self._dao.get(session)
        return list

    async def get_by_id(self, id: int, session: AsyncSession) -> T:
        obj = await self._dao.get_by_id(id, session)
        if not obj:
            raise HTTPException(status_code=404, detail="Object not found")
        return obj

    async def create(self, data: CreateSchema, session: AsyncSession) -> T:
        pass

    async def update(self, id: int, data: UpdateSchema, session: AsyncSession) -> T:
        pass

    async def delete(self, id: int, session: AsyncSession) -> None:
        await self._dao.delete(id, session)
