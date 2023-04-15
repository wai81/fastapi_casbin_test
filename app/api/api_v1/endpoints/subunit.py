from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
# from sqlalchemy.orm import Session
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud
from app.api.depend import get_db, get_current_user
from fastapi_pagination import paginate, Page

from app.modules.subunit.filter import SubunitListFilter
from app.modules.subunit.schema import SubunitCreate, SubunitUpdate, SubunitInDB
from app.modules.user.schema import User

router = APIRouter()


@router.get("/",
            status_code=200,
            # response_model=List[Subunit]
            response_model=Page[SubunitInDB]
            )
async def subunits(
       filters: SubunitListFilter = FilterDepends(SubunitListFilter),
        *, db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
) -> Any:
    """
    All subunits
    """
    # objects = await crud.subunit.get_all(db=db, sort=sort, order=order)
    objects = await crud.subunit.get_subunits_filter(db=db, filters=filters)
    result = paginate(objects)
    return result


@router.get("/{subunit_id}", status_code=200, response_model=SubunitInDB)
async def get_subunit(
        *,
        subunit_id: str,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
) -> dict:
    """
    Subunit by ID
    """
    objects = await crud.subunit.get(db=db, id=subunit_id)
    return objects


@router.post("/", status_code=201, response_model=SubunitInDB)
async def create_subunit(
        *,
        request: SubunitCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
) -> dict:
    """
    Create subunit
    """
    obj = await crud.subunit.get_by_name(db=db, name=request.name, tor_id=request.organization_id)
    if obj:
        raise HTTPException(
            status_code=400, detail=f"Name subunit in TOR: {request.name} is exist."
        )
    if not request.organization_id:
        raise HTTPException(
            status_code=400, detail=f"Not selected organization. Organization required"
        )
    result = await crud.subunit.create(db=db, request=request)
    return result


@router.put("/{subunit_id}", status_code=201, response_model=SubunitInDB)
async def update_subunit(
        *,
        subunit_id: str,
        request: SubunitUpdate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
) -> dict:
    """
    Update subunit
    """
    obj = await crud.subunit.get(db=db, id=subunit_id)
    if not obj:
        raise HTTPException(
            status_code=400, detail=f"Organization with ID: {subunit_id} not found."
        )
    result = await crud.subunit.update(db=db, db_obj=obj, request=request)
    return result


@router.delete("/{subunit_id}", status_code=200)
async def delete_organization(
        *,
        subunit_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    Delete subunit
    """
    obj = await crud.subunit.get(db=db, id=subunit_id)
    if not obj:
        raise HTTPException(
            status_code=400, detail=f"Item with ID: {subunit_id} not found."
        )
    return await crud.subunit.remove(db=db, db_obj=obj)

