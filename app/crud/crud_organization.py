# from sqlalchemy.orm import Session
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, subqueryload

from app.crud.base import CRUDBase
from app.modules.organization.filter import OrganizationFilter
from app.modules.organization.model import Organization
from app.modules.organization.schema import OrganizationCreate, OrganizationUpdate


class CRUDOrganization(CRUDBase[Organization, OrganizationCreate, OrganizationUpdate]):

    async def get_by_torid(self, db: AsyncSession, *, id: int) -> Organization:
        # query = await db.query(Organization)
        # return query.filter(Organization.id == id).first()
        query = select(Organization). \
            where(Organization.id == id). \
            options(joinedload('subunits'))

        result = await db.execute(query)
        return result.scalar()

    async def get_organiztions_subunits(self, db: AsyncSession) -> List[Organization]:
        query = select(Organization).options(subqueryload(Organization.subunits)).order_by(Organization.id)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_organiztions_filter(self, db: AsyncSession, *, filters: OrganizationFilter) -> List[Organization]:
        query = select(Organization)
        query = filters.filter(query)
        query = filters.sort(query)
        result = await db.execute(query)
        return result.scalars().all()


organization = CRUDOrganization(Organization)
