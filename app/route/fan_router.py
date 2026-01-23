from fastapi import APIRouter

fan_router = APIRouter()

@fan_router.get('/')
async def fan_get():
    return {'message': 'fan'}
