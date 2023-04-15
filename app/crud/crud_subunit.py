# from sqlalchemy.orm import Session
from operator import or_
from typing import List, Union, Dict, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from app.crud.base import CRUDBase
from app.modules.subunit.filter import SubunitListFilter
from app.modules.subunit.model import Subunit
from app.modules.organization.model import Organization
from app.modules.subunit.schema import SubunitCreate, SubunitUpdate
from app import crud


class CRUDSubunit(CRUDBase[Subunit, SubunitCreate, SubunitUpdate]):

    async def get_by_name(self, db: AsyncSession, *, name: str, tor_id: int):
        # query = await db.query(Organization)
        # return query.filter(Organization.id == id).first()
        query = select(Subunit).where(Subunit.name == name,
                                      Subunit.organization_id == tor_id)
        result = await db.execute(query)
        return result.scalar()

    async def get_all(self, db: AsyncSession, *,
                      sort: str = None,
                      order: str = None,
                      filters: str = None,
                      ) -> List[Subunit]:

        query = select(Subunit). \
            options(joinedload('organization'))
        if filters is not None and filters != "null":
            # we need filter format data like this  --> {'name': 'an','country':'an'}
            # convert string to dict format

            criteria = dict(x.split("*") for x in filters.split('-'))
            criteria_list = []

            # check every key in dict. are there any table attributes that are the same as the dict key ?
            for attr, value in criteria.items():
                _attr = getattr(self.model, attr)

                # filter format
                search = "%{}%".format(value)

                # criteria list
                criteria_list.append(_attr.like(search))

            query = query.filter(or_(*criteria_list))

        if sort is not None and sort != "null":
            if sort == '"organization.name"':
                sort = "name_1"
            # we need sort format data like this --> ['id','name']
            if order is not None and order != "null":
                if order == '"DESC"':
                    query = query.order_by(desc(text(self.convert_sort(sort))))
            query = query.order_by(text(self.convert_sort(sort)))

        result = await db.execute(query)
        return result.scalars().all()

        result = await db.execute(query)
        return result.scalars().all()

    async def get_subunits_filter(self, db: AsyncSession, *, filters: SubunitListFilter):
        query = select(Subunit).join(Organization)
        query = filters.filter(query)
        query = filters.sort(query)
        result = await db.execute(query)
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, request: SubunitCreate) -> Subunit:
        create_data = request.dict()
        obj = Subunit(**create_data)
        selected_organization = await crud.organization.get_by_torid(db=db, id=request.organization_id)
        obj.title = f'{request.name} ({selected_organization.title})'
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def update(self, db: AsyncSession, *,
                     db_obj: Subunit, request: Union[SubunitUpdate, Dict[str, Any]]) -> Subunit:

        # obj = await self.get(db=db, id=db_obj.id)
        obj_data = jsonable_encoder(db_obj)
        selected_organization = await crud.organization.get_by_torid(db=db, id=request.organization_id)
        organization_title = selected_organization.title

        if isinstance(request, dict):
            update_data = request
            # update_data['title'] = f'{request.name} ({organization_title})'

        else:
            update_data = request.dict(exclude_unset=True)
        #     update_data['title'] = f'{request.name} ({organization_title})'
        # for var, value in vars(db_obj).items():
        #     setattr(db_obj, var, value) if value else None
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])


        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


subunit = CRUDSubunit(Subunit)
