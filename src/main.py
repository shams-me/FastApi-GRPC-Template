import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import create_async_engine

from src.core.logger import LOGGING
from src.connections import postgres, redis_cli
from src.settings import settings

from src.api import routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    postgres.engine = create_async_engine(
        url=settings.pg_dsn
    )
    redis_cli.redis = Redis(host=settings.redis_host, port=settings.redis_port)

    yield

    await redis_cli.redis.close()
    await postgres.engine.dispose()


app = FastAPI(
    title=settings.project_name,
    lifespan=lifespan,
    version="1.0.0",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
async def ping():
    return {"message": "pong"}


app.include_router(routes.router, prefix="/users/api")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=settings.REST_PORT,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
