import enum
from datetime import datetime
from uuid import UUID

import jwt
from fastapi import Depends
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer
from jwt import ExpiredSignatureError
from pydantic import BaseModel

from src.rpc.user.client import UserRpc
from src.settings import settings

jwt_token_key_header = HTTPBearer()


class User(BaseModel):
    id: UUID
    name: str
    roles: list[str | None]

    class Config:
        extra = "allow"


class RoleOptions(str, enum.Enum):
    SUPERUSER = "superuser"
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"


async def access_control(
        token: str,
        roles: list[RoleOptions | None] = RoleOptions.SUPERUSER,
        verified_user: bool = False
) -> bool:
    """
    
    :param rpc:
    :param token: JWT
    :param roles: List of role who can get access to that route
    :param verified_user: If True user will ask auth service otherwise it just decodes token  
    :return: 
    """
    if verified_user:
        async with UserRpc(settings.user_service_host, settings.user_service_port).connect() as user_rpc:
            user = await user_rpc.get_user(token=token)
    else:
        user = _decode_and_check_token(secret_key=settings.auth_jwt_secret_key, token=token)

    if RoleOptions.SUPERUSER in user.roles:
        return True

    if set(user.roles).intersection(roles):
        return True

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You don't have enough permissions",
    )


def _decode_and_check_token(secret_key: str, token: str, algorithm: str = "HS256") -> User:
    """
    Decodes a JWT token and checks if it has expired.
    Raises an exception if the token has expired.

    :param secret_key: Secret key used for decoding.
    :param token: The JWT token to be decoded.
    :param algorithm: Algorithm used for decoding (default: HS256).
    :return: Decoded JWT token payload as a dictionary.
    :raises HTTPException: If the token is expired or invalid.
    """
    try:
        # Decode the token
        decoded_payload = jwt.decode(token, key=secret_key, algorithms=[algorithm])

        # Check if the token has expired
        expiration_time = decoded_payload.get("exp")
        current_time = int(datetime.utcnow().timestamp())
        if expiration_time and expiration_time <= current_time:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired.")

        return User(**decoded_payload)

    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired.")
    except jwt.DecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token could not be decoded.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def super_user_access(token=Depends(jwt_token_key_header)):
    return await access_control(roles=[RoleOptions.SUPERUSER], verified_user=True, token=token.credentials)
