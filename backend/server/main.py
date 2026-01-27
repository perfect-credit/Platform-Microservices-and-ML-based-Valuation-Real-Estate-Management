from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.events.startup import app_lifespan


def app():
    api = FastAPI(lifespan=app_lifespan)
    api.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return api
