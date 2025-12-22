from fastapi import APIRouter

fa_router = APIRouter()

@fa_router.get('/')
async def fa_get():
    return {'message': 'fa'}
