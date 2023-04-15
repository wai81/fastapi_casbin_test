import random
import shutil
import string
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from fastapi_filter import FilterDepends
from fastapi_pagination import paginate, Page
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api.depend import get_db, get_current_user, get_current_active_superuser
from app.modules.user.filter import UserFilter
from app.modules.user.schema import UserInDB, UserProfile, UserCreate, UserUpdate, User

router = APIRouter()


@router.get("/", status_code=200,
            response_model=Page[UserInDB]
            )
async def all_users_offset(
        filters: UserFilter = FilterDepends(UserFilter),
        *, db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
) -> Any:
    """
    Cписок пользователей
    """
    # objects = await crud.user.get_all(db=db, sort=sort, order=order)
    if current_user.is_active:
        # if not current_user.is_superuser:
        #     raise HTTPException(
        #         status_code=406,
        #         detail="Permission denied",
        #     )

        objects = await crud.user.get_users_filter(db=db, filters=filters)
        result = paginate(objects)
    else:
        raise HTTPException(
            status_code=401,
            detail="The user is not activate!",
        )
    return result


@router.get("/{user_id}", status_code=200, response_model=UserProfile)
async def get_user_by_id(
        *,
        user_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
) -> dict:
    """
    Пользователь по id
    """

    obj = await crud.user.get(db=db, id=user_id)
    return obj


@router.post("/", status_code=201, response_model=UserProfile)
async def create_user(
        *, db: AsyncSession = Depends(get_db),
        user_in: UserCreate,
        current_user: User = Depends(get_current_active_superuser)
) -> dict:
    """
    Create new user
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
    result = await crud.user.create(db=db, request=new_user)

    return result


@router.post('/upload/avatar')
def upload_image(image: UploadFile = File(...),
                 current_user: User = Depends(get_current_user)
                 ):
    letters = string.ascii_letters
    rand_str = ''.join(random.choice(letters) for i in range(6))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit('.', 1))
    path = f'media/user_avatars/{filename}'

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {'url': path}


@router.put("/{user_id}", status_code=201, response_model=UserProfile)
async def update_user(
        *,
        user_id: UUID,
        request: UserUpdate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_active_superuser)
) -> dict:
    """
    Update user
    """

    obj = await crud.user.get(db=db, id=user_id)
    if not obj:
        raise HTTPException(
            status_code=400, detail=f"User with ID: {user_id} not found."
        )
    result = await crud.user.update(db=db, db_obj=obj, request=request)
    return result


@router.delete("/{user_id}", status_code=200)
async def delete_user(
        *,
        user_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_active_superuser),
):
    """
    Delete user
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=406,
            detail="Permission denied",
        )

    obj = await crud.user.get(db=db, id=user_id)
    if not obj:
        raise HTTPException(
            status_code=400, detail=f"Item with ID: {user_id} not found."
        )
    return await crud.user.remove(db=db, db_obj=obj)
