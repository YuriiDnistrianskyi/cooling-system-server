from fastapi import APIRouter

device_router = APIRouter()

@device_router.get('/')
def device_get():
    pass

@device_router.post('/')
def device_post():
    pass
