from fastapi import APIRouter

from server.routers.ads import v1


def router_factory() -> APIRouter:
    router = APIRouter(prefix="")

    router.include_router(v1.router_factory())

    return router
