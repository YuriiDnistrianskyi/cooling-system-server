from fastapi import FastAPI, APIRouter
from .route import *

def create_app() -> FastAPI:
    app: FastAPI = FastAPI()

    init_db(app)
    connect_router(app)

    return app

def init_db(app: FastAPI) -> None:
    pass
