from typing import Any
from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud
from app.api.depend import get_db, get_current_user
from fastapi_pagination import paginate, Page

from app.modules.booking_transport.filter import BookingTransportListFilter
from app.modules.booking_transport.schema import BookingTransportCreate, BookingTransportUpdate, \
    BookingTransportInDB
from app.modules.user.model import User

router = APIRouter()


@router.get("/",
            status_code=200,
            # response_model=List[Subunit]
            response_model=Page[BookingTransportInDB]
            )
async def bookings(*,
                   filters: BookingTransportListFilter = FilterDepends(BookingTransportListFilter),
                   db: AsyncSession = Depends(get_db),
                   # current_user: User = Depends(get_current_user)
                   ) -> Any:
    """
    All bookings
    """
    # objects = await crud.booking_transport.get_all(db=db)
    objects = await crud.booking_transport.get_boking_transport_filter(db=db, filters=filters)
    result = paginate(objects)
    return result


@router.get("/{booking_id}", status_code=200, response_model=BookingTransportInDB)
async def get_booking(
        *,
        booking_id: str,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
) -> dict:
    """
    Booking by ID
    """
    objects = await crud.booking_transport.get(db=db, id=booking_id)
    return objects


@router.post("/", status_code=201, response_model=BookingTransportInDB)
async def create_booking(
        *,
        request: BookingTransportCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
) -> dict:
    """
    Create booking
    """
    # obj = await crud.booking_transport.get(db=db, name=request.name)
    # if not obj:
    #     raise HTTPException(
    #         status_code=400, detail=f"Booking transport with ID: {request.id} is exist."
    #     )
    result = await crud.booking_transport.create(db=db, request=request)
    return result


@router.put("/{booking_id}", status_code=201, response_model=BookingTransportInDB)
async def update_booking(
        *,
        booking_id: str,
        request: BookingTransportUpdate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
) -> dict:
    """
    Update booking
    """
    obj = await crud.booking_transport.get(db=db, id=booking_id)
    if not obj:
        raise HTTPException(
            status_code=400, detail=f"Item with ID: {booking_id} not found."
        )
    result = await crud.booking_transport.update(db=db, db_obj=obj, request=request)
    return result


@router.delete("/{booking_id}", status_code=200)
async def delete_booking(
        *,
        booking_id: str,
        db: AsyncSession = Depends(get_db)
):
    """
    Delete booking
    """
    obj = await crud.booking_transport.get(db=db, id=booking_id)
    if not obj:
        raise HTTPException(
            status_code=400, detail=f"Item with ID: {booking_id} not found."
        )
    return await crud.booking_transport.remove(db=db, db_obj=obj)
