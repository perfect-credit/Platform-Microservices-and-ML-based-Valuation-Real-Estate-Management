from fastapi import APIRouter

from server.config import settings
from server.schemas.responses.health import HealthResponse


def router_factory() -> APIRouter:
    router = APIRouter(prefix="/health", tags=["Health Check"])

    @router.get("", response_model=HealthResponse)
    async def health():
        return settings.model_dump()

    return router
