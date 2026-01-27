import asyncio
import logging
from concurrent import futures

from grpc.experimental import aio

from config import settings
from pb.valuation_pb2_grpc import add_ValuationServiceServicer_to_server
from services import ValuationService


async def serve():
    server = aio.server(futures.ThreadPoolExecutor(max_workers=10))

    add_ValuationServiceServicer_to_server(ValuationService(), server)

    server.add_insecure_port(f"[::]:{settings.PORT}")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    logging.info("Starting server")
    print(f"Server running on port {settings.PORT}")
    asyncio.run(serve())
