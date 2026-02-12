from app.db.database import async_session

async def get_async_session():
    async with async_session() as session:
        yield session

def get_session_factory():
    return async_session
