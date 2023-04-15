import shutil
import string
import random
from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi_filter import FilterDepends
from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api.depend import get_db, get_current_user
from app.modules.booking_transport.filter import TransportListFilter
from app.modules.booking_transport.schema import Transport, TransportCreate, TransportUpdate, TransportInDB
from app.modules.user.schema import User

router = APIRouter()


@router.get("/",
            status_code=200,
            response_model=Page[TransportInDB])
async def transport(
        filters: TransportListFilter = FilterDepends(TransportListFilter),
        *, db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
) -> Any:
    """
    All images offset
    """
    objects = await crud.transport.get_transport_filter(db=db, filters=filters)
    result = paginate(objects)
    return result


@router.get("/all",
            status_code=200,
            response_model=List[TransportInDB])
async def all_transport(
        *,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
) -> Any:
    """
    All images
    """
    objects = await crud.transport.get_all(db=db)
    result = objects
    return result


@router.get("/{transport_id}",
            status_code=200,
            response_model=TransportInDB)
async def get_transport(
        *,
        transport_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
) -> dict:
    """
    Transport by ID
    """
    object = await crud.transport.get(db=db, id=transport_id)
    return object


@router.post("/",
             status_code=201,
             response_model=TransportInDB)
async def create_transport(
        *,
        request: TransportCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
) -> dict:
    """
    Create images
    """
    result = await crud.transport.create(db=db, request=request)
    return result


@router.post('/image')
def upload_image(image: UploadFile = File(...),
                 current_user: User = Depends(get_current_user)
                 ):

    letters = string.ascii_letters
    rand_str = ''.join(random.choice(letters) for i in range(6))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit('.', 1))
    path = f'media/transports/{filename}'

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {'url': path}


@router.put("/{transport_id}",
            status_code=201,
            response_model=TransportInDB)
async def update_transport(
        *,
        transport_id: UUID,
        request: TransportUpdate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)) -> dict:
    """
    Update images
    """
    obj = await crud.transport.get(db=db, id=transport_id)
    if not obj:
        raise HTTPException(
            status_code=400, detail=f"Item with ID:: {transport_id} not found."
        )
    result = await crud.transport.update(db=db, db_obj=obj, request=request)
    return result


@router.delete("/{transport_id}",
               status_code=200)
async def delete_transport(
        *,
        transport_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    """
    Delete images
    """
    obj = await crud.transport.get(db=db, id=transport_id)
    if not obj:
        raise HTTPException(
            status_code=400, detail=f"Item with ID: {transport_id} not found."
        )
    return await crud.transport.remove(db=db, db_obj=obj)
