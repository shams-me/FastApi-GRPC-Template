import asyncio
import logging

import grpc
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import create_async_engine

from rpc.user import user_pb2_grpc
from src.connections import postgres, redis_cli
from src.rpc.user.service import GRPCUserService
from src.settings import settings

logging.basicConfig(level=logging.INFO)

_cleanup_coroutines = []


async def serve() -> None:
    postgres.engine = create_async_engine(
        url=settings.pg_dsn
    )
    redis_cli.redis = Redis(host=settings.redis_host, port=settings.redis_port)

    server = grpc.aio.server()
    user_pb2_grpc.add_UserServicer_to_server(GRPCUserService(), server)
    server.add_insecure_port(f"[::]:{settings.GRPC_PORT}")
    await server.start()
    logging.info(f"GRPC Server running http://127.0.0.1:{settings.GRPC_PORT} (Press CTRL+C to quit)")

    async def graceful_shutdown():
        print("Graceful shutdown countdown...")
        await server.stop(5)
        print("Shutting down...")

    _cleanup_coroutines.append(graceful_shutdown())
    await server.wait_for_termination()

    await redis_cli.redis.close()
    await postgres.engine.dispose()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(serve())
    finally:
        loop.run_until_complete(*_cleanup_coroutines)
        loop.close()
