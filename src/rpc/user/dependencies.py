from src.connections.redis_cli import redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.connections import postgres
from src.services.auth import AuthServiceImpl
from src.settings import settings
from src.utils.token_encoder import JWTEncoder
from src.utils.token_handler import JWTHandler


class UserServiceWrapper:
    session: AsyncSession

    async def __aenter__(self):
        self.session = AsyncSession(postgres.engine, expire_on_commit=False)
        token_encoder = JWTEncoder(secret=settings.auth_jwt_secret_key)
        token_handler = JWTHandler(encoder=token_encoder)
        return AuthServiceImpl(session=self.session, token_handler=token_handler, redis=redis)

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.aclose()
