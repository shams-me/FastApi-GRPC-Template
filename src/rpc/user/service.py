import grpc

from src.models.user import User
from src.rpc.user.dependencies import UserServiceWrapper
from src.rpc.user.user_pb2 import UserInfoResponse, UserInfoByTokenRequest
from src.rpc.user.user_pb2_grpc import UserServicer


class GRPCUserService(UserServicer):
    @staticmethod
    async def __generate_response(
            request: UserInfoByTokenRequest,
            context: grpc.aio.ServicerContext,
            user: User | None
    ) -> UserInfoResponse:
        response = UserInfoResponse()

        if user is None:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            return response
        roles = list([role.name for role in await user.awaitable_attrs.roles])
        return UserInfoResponse(
            id=str(user.id),
            name=user.name,
            roles=roles
        )

    async def GetUserInfoByToken(
            self,
            request: UserInfoByTokenRequest,
            context: grpc.aio.ServicerContext
    ) -> UserInfoResponse:
        async with UserServiceWrapper() as user_service:
            user = user_service.token_handler.decode(request.token)
            user = await user_service.get_user(user.get("id"))
        return await GRPCUserService.__generate_response(request, context, user)
