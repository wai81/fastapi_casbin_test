from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud
from app.api.depend import get_db, get_current_user
from app.core.auth import authenticate, create_access_token
from app.modules.user.schema import User, UserLogin, RegisterUser

router = APIRouter()


@router.post("/login",
             # response_model=User
             )
async def login(
        *,
        db: AsyncSession = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Get the JWT for a user with data from OAuth2 request form body.
    """

    user = await authenticate(username=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # result = User(username=user.username,
    #               first_name=user.first_name,
    #               last_name=user.last_name,
    #               patronymic=user.patronymic,
    #               is_superuser=user.is_superuser,
    #               id=user.id,
    #               access_token=create_access_token(sub=user.id))
    # return result
    return {
        "access_token": create_access_token(sub=user.id),
        "token_type": "bearer",
    }


@router.post("/user/signin", response_model=User)
async def user_signin(
        *,
        db: AsyncSession = Depends(get_db),
        form_data: UserLogin,
) -> Any:
    """
    Get JWT for user with from request
    """

    user = await authenticate(username=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    result = User(username=user.username,
                  first_name=user.first_name,
                  last_name=user.last_name,
                  patronymic=user.patronymic,
                  is_superuser=user.is_superuser,
                  is_active=user.is_active,
                  organization=user.organization,
                  access_tors=user.access_tors,
                  avatar=user.avatar,
                  id=user.id,
                  access_token=create_access_token(sub=user.id))
    return result
    # return {
    #     "access_token": create_access_token(sub=user.id),
    #     "token_type": "bearer",
    # }


@router.get("/user", response_model=User)
async def read_users_me(
        current_user: User = Depends(get_current_user)
):
    """
    Fetch the current logged in user.
    """

    user = current_user

    result = User(username=user.username,
                  first_name=user.first_name,
                  last_name=user.last_name,
                  patronymic=user.patronymic,
                  is_superuser=user.is_superuser,
                  is_active=user.is_active,
                  organization=user.organization,
                  access_tors=user.access_tors,
                  avatar=user.avatar,
                  id=user.id,
                  created_at=user.created_at,
                  access_token=create_access_token(sub=user.id))

    # return user
    return result


@router.post("/user/signup", response_model=User, status_code=201)
async def create_user_signup(
        *, db: AsyncSession = Depends(get_db),
        user_in: RegisterUser,
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    new_user = user_in

    if new_user.username.strip() == '':
        raise HTTPException(
            status_code=422,
            detail="The username is required",
        )
    if new_user.password.strip() == '':
        raise HTTPException(
            status_code=422,
            detail="Password required",
        )
    user = await crud.user.get_by_username(db=db, username=new_user.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    obj = await crud.user.create(db=db, request=new_user)

    create_access_token(sub=obj.id)

    result = User(username=obj.username,
                  first_name=obj.first_name,
                  last_name=obj.last_name,
                  patronymic=obj.patronymic,
                  is_superuser=obj.is_superuser,
                  id=obj.id,
                  access_token=create_access_token(sub=obj.id))
    return result
