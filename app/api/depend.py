from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import Session

from jose import jwt, JWTError
from sqlalchemy.future import select

from app import crud
from app.core.auth import oauth2_scheme
from app.core.config import settings
# from app.db.session import SessionLocal
from app.db.session_async import SessionLocalAsync
from app.modules.user.model import User


class TokenData(BaseModel):
    username: Optional[str] = None


# def get_db() -> Generator:
#     db = SessionLocal()
#     db.current_user_id = None
#     try:
#         yield db
#     finally:
#         db.close()

async def get_db() -> Generator:
    db = SessionLocalAsync()
    db.current_user_id = None
    try:
        yield db
        await db.commit()
    finally:
        await db.close()


async def get_current_user(
        db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    query = select(User).where(User.id == token_data.username)
    result = await db.execute(query)
    user = result.scalars().first()
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not await crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=406, detail="The user doesn't have enough privileges"
        )
    return current_user
