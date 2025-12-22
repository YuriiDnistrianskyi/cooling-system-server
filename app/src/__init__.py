from fastapi import FastAPI, APIRouter
from .route import *

def create_app() -> FastAPI:
    app: FastAPI = FastAPI()

    connect_router(app)

    return app
