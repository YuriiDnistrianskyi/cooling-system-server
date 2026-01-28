from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict

class GeneralService:
    _class_type = None
    _dao = None
    _create_schema = None
    _update_schema = None

    async def get(self, session: AsyncSession) -> List[self._class_type]:
        list = await self._dao.get(session)
        return list

    async def create(self, data: _create_schema, session: AsyncSession) -> self._class_type:
        pass

    async def update(self, id: int, data: self._update_schema, session: AsyncSession) -> self._class_type:
        pass

    async def delete(self, id: int, session: AsyncSession) -> None:
        self._dao.delete(id, session)
