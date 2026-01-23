from fastapi import APIRouter

cpu_router = APIRouter()

@cpu_router.get('/')
async def get():
    return {"message": "cpu"}
