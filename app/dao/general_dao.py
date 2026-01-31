from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import TypeVar, Generic, List, Any, Type

T: Any = TypeVar("T")

class GeneralDao(Generic[T]):
    _class_type: Type[T]

    async def get(self, session: AsyncSession) -> List[T]:
        stmt = select(self._class_type)
        list = await session.execute(stmt)
        result = list.scalars().all()
        return result

    async def create(self, obj: T, session: AsyncSession) -> T:
        session.add(obj)
        return obj

    async def update(self, id: int, session: AsyncSession) -> T:
        obj = await session.get(self._class_type, id)
        if not obj:
            raise HTTPException(status_code=404, detail="Object not found")
        return obj

    async def delete(self, id: int, session: AsyncSession) -> None:
        obj = await session.get(self._class_type, id)
        if not obj:
            raise HTTPException(status_code=404, detail="Object not found")
        await session.delete(obj)
