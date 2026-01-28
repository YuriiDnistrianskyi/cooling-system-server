from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict

class GeneralDao:
    _class_type = None

    async def get(self, session: AsyncSession) -> List[self._class_type]:
        stmt = select(self._class_type)
        list = await session.execute(stmt)
        result = list.scalars().all()
        return result

    async def create(self, obj: self._class_type, session: AsyncSession) -> self._class_type:
        session.add(obj)
        return obj

    async def update(self, id: int, obj: self._class_type, session: AsyncSession) -> self._class_type:
        obj = await session.get(self._class_type, id)
        if not old_obj:
            raise HTTPException(status_code=404, detail="Object not found")
        return obj

    async def delete(self, id: int, session: AsyncSession) -> None:
        obj = await session.get(self._class_type, id)
        if not obj:
            raise HTTPException(status_code=404, detail="Object not found")
        await session.delete(obj)
