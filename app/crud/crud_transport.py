from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.base import CRUDBase
from app.modules.booking_transport.filter import TransportFilter
from app.modules.booking_transport.model import Transport
from app.modules.booking_transport.schema import TransportCreate, TransportUpdate


class CRUDTransport(CRUDBase[Transport, TransportCreate, TransportUpdate]):

    async def get_transport_filter(self, db: AsyncSession, *, filters: TransportFilter) -> List[Transport]:
        query = select(Transport)
        query = filters.filter(query)
        query = filters.sort(query)
        result = await db.execute(query)
        return result.scalars().all()


transport = CRUDTransport(Transport)
