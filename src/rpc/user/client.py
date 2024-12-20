from contextlib import asynccontextmanager
from http import HTTPStatus

import grpc
from fastapi import HTTPException
from grpc.aio import AioRpcError

from . import user_pb2
from . import user_pb2_grpc


class UserRpc:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.channel = None
        self.stub = None

    @asynccontextmanager
    async def connect(self):
        """Establish a connection to the server and ensure it's closed afterward."""
        self.channel = grpc.aio.insecure_channel(f'{self.host}:{self.port}')
        self.stub = user_pb2_grpc.UserStub(self.channel)
        try:
            yield self
        finally:
            await self.close()

    async def get_user(self, token: str):
        """Fetch user info based on the token."""
        if not self.stub:
            raise HTTPException(status_code=500, detail="Connection is not established.")
        try:
            request = user_pb2.UserInfoByTokenRequest(token=token)
            response = await self.stub.GetUserInfoByToken(request)
            return response
        except AioRpcError as e:
            if e.code() == grpc.StatusCode.UNAUTHENTICATED:
                raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=e.details())
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def close(self):
        """Close the connection."""
        if self.channel:
            await self.channel.close()
