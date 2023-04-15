from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, Query
# from sqlalchemy.orm import Session
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud
from app.api.depend import get_db, get_current_user, get_current_active_superuser
from fastapi_pagination import paginate, Page

from app.modules.organization.filter import OrganizationListFilter
from app.modules.organization.schema import Organization, OrganizationCreate, OrganizationUpdate
from app.modules.subunit.schema_organizations_subunits import OrganizationSubunits
from app.modules.user.schema import User

router = APIRouter()


@router.get("/",
            status_code=200,
            # response_model=List[Organization]
            response_model=Page[Organization])
async def organizations(
        filters: OrganizationListFilter = FilterDepends(OrganizationListFilter),
        *, db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
) -> Any:
    """
    All organizations offset
    """
    objects = await crud.organization.get_organiztions_filter(db=db, filters=filters)
    result = paginate(objects)
    return result


@router.get("/all",
            status_code=200,
            response_model=List[Organization])
async def all_organizations(
        *,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
) -> Any:
    """
    All organizations
    """
    objects = await crud.organization.get_all(db=db)
    result = objects
    return result


@router.get("/{organization_id}",
            status_code=200,
            response_model=Organization)
async def get_organization(
        *,
        organization_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
) -> dict:
    """
    Organization by ID
    """
    object = await crud.organization.get(db=db, id=organization_id)
    return object


@router.get("/all/subunits", status_code=200, response_model=List[OrganizationSubunits])
async def get_organizations_subunits(
        *,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
) -> dict:
    """
    Get All Organizations Subunits
    """
    objects = await crud.organization.get_organiztions_subunits(db=db)
    return objects


@router.get("/{organization_id}/subunits",
            status_code=200,
            response_model=OrganizationSubunits)
async def get_subunits_by_organization_id(
        *,
        organization_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
) -> dict:
    """
    Organization Subunits by ID
    """
    objects = await crud.organization.get_by_torid(db=db, id=organization_id)
    return objects


@router.post("/",
             status_code=201,
             response_model=Organization)
async def create_organization(
        *,
        request: OrganizationCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_active_superuser)
) -> dict:
    """
    Create organization
    """
    obj = await crud.organization.get_by_torid(db=db, id=request.id)
    if obj:
        raise HTTPException(
            status_code=400, detail=f"Recipe with TOR: {request.id} is exist."
        )
    result = await crud.organization.create(db=db, request=request)
    return result


@router.put("/{organization_id}",
            status_code=201,
            response_model=Organization)
async def update_organization(
        *,
        organization_id: int,
        request: OrganizationUpdate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_active_superuser),
) -> dict:
    """
    Update organization
    """
    obj = await crud.organization.get(db=db, id=organization_id)
    if not obj:
        raise HTTPException(
            status_code=400, detail=f"Organization with ID: {organization_id} not found."
        )
    result = await crud.organization.update(db=db, db_obj=obj, request=request)
    return result


@router.delete("/{organization_id}",
               status_code=200)
async def delete_organization(
        *,
        organization_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_active_superuser),
):
    """
    Delete organization
    """
    obj = await crud.organization.get(db=db, id=organization_id)
    if not obj:
        raise HTTPException(
            status_code=400, detail=f"Item with ID: {organization_id} not found."
        )
    return await crud.organization.remove(db=db, db_obj=obj)
