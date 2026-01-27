import asyncio
from pathlib import Path
from types import ModuleType

import aiofiles
from fastapi import FastAPI
from starlette.routing import BaseRoute

from server.config import settings


def find_services() -> list[ModuleType]:
    # all the services are stored in the `server/routes` folder
    services = []
    for item in Path("server/routers").iterdir():
        if item.is_dir() and item.name not in {"__pycache__", "docs"}:
            # import the module dynamically
            module = __import__(f"server.routers.{item.name}", fromlist=[""])
            services.append(module)

    return services


async def add_endpoint_description(route: BaseRoute) -> None:
    directory = __name__.replace(".", "/")
    docs_file = f"{directory}/docs{route.path}.md"

    try:
        # documentation is stored in a markdown file with the same path as the route in the `docs` folder
        async with aiofiles.open(docs_file) as reader:
            description = await reader.read()
    except FileNotFoundError:
        raise ValueError(f"Documentation file for {route.path} in {docs_file} not found")

    # Enforce that the description is not empty
    if not description.strip():
        raise ValueError(f"Description for {route.path} in {docs_file} is empty")

    route.description = description


async def register_routers(app: FastAPI) -> FastAPI:
    tasks = []

    for service in find_services():
        router = service.router_factory()
        for route in router.routes:
            tasks.append(add_endpoint_description(route))

        await asyncio.gather(*tasks, return_exceptions=True)
        app.include_router(router, prefix=settings.API_PREFIX)

    return app
