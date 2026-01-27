from contextlib import asynccontextmanager

from fastapi import FastAPI

from server.routers import register_routers


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    print("Running application initialization steps ...")

    await register_routers(app)
    yield

    print("Running application cleanup steps ...")
