import asyncio
import logging
from concurrent import futures

from grpc.experimental import aio

from config import settings
from events import startup
from pb.auth_pb2_grpc import add_AuthServiceServicer_to_server
from services import AuthService


async def serve():
    await startup()
    server = aio.server(futures.ThreadPoolExecutor(max_workers=10))

    add_AuthServiceServicer_to_server(AuthService(), server)

    server.add_insecure_port(f"[::]:{settings.PORT}")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    logging.info("Starting server")
    print(f"Server running on port {settings.PORT}")
    asyncio.run(serve())
