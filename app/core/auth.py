from datetime import datetime, timedelta
from typing import Optional, MutableMapping, Union, List

from fastapi.security import OAuth2PasswordBearer
# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from sqlalchemy.future import select

from app.core.config import settings
from app.core.security import verify_password
from app.modules.user.model import User

JWTPayloadMapping = MutableMapping[
    str, Union[datetime, bool, str, List[str], List[int]]
]

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/auth/login")


async def authenticate(*, username: str, password: str, db: AsyncSession, ) -> Optional[User]:
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    user = result.scalars().first()
    # user = await db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(*, sub: str) -> str:
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )


def _create_token(token_type: str, lifetime: timedelta, sub: str, ) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type

    # https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3
    # The "exp" (expiration time) claim identifies the expiration time on
    # or after which the JWT MUST NOT be accepted for processing
    payload["exp"] = expire

    # The "iat" (issued at) claim identifies the time at which the
    # JWT was issued.
    payload["iat"] = datetime.utcnow()

    # The "sub" (subject) claim identifies the principal that is the
    # subject of the JWT
    payload["sub"] = str(sub)
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
