# from sqlalchemy.orm import Session
from datetime import timezone
from typing import List, Union, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from app.crud.base import CRUDBase
from app.modules.booking_transport.model import BookingTransport, Transport
from app.modules.booking_transport.schema import BookingTransportCreate, BookingTransportUpdate
from app.modules.organization.model import Organization
from app.modules.subunit.model import Subunit


class BookingTransportFilter:
    pass


class CRUDBookingTransport(CRUDBase[BookingTransport, BookingTransportCreate, BookingTransportUpdate]):

    async def get(self, db: AsyncSession, id: str) -> BookingTransport:
        query = select(BookingTransport). \
            where(BookingTransport.id == id). \
            options(joinedload('subunit')). \
            options(joinedload('organization')).\
            options(joinedload('transport'))

        result = await db.execute(query)
        return result.scalars().first()

    async def get_all(self, db: AsyncSession, ) -> List[BookingTransport]:
        query = select(BookingTransport). \
            options(joinedload('subunit')). \
            options(joinedload('organization')). \
            options(joinedload('transport'))
        result = await db.execute(query)
        return result.scalars().all()

    async def get_boking_transport_filter(
            self, db: AsyncSession, *,
            filters: BookingTransportFilter) -> List[BookingTransport]:
        query = select(BookingTransport). \
            join(Organization). \
            join(BookingTransport.subunit). \
            outerjoin(Transport)
            # options(joinedload('subunit')). \
            # options(joinedload('organization')). \
            # options(joinedload('transport'))
        query = filters.filter(query)
        query = filters.sort(query)
        result = await db.execute(query)
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, request: BookingTransportCreate) -> BookingTransport:
        create_data = request.dict()
        create_data.pop("startDate")
        create_data.pop("endDate")
        obj = BookingTransport(**create_data)
        # obj.hashed_password = get_password_hash(request.password)

        obj.startDate = request.startDate.replace(tzinfo=timezone.utc)
        obj.endDate = request.endDate.replace(tzinfo=timezone.utc)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def update(self, db: AsyncSession, *, db_obj: BookingTransport,
                     request: Union[BookingTransportUpdate, Dict[str, Any]]) -> BookingTransport:

        if isinstance(request, dict):
            update_data = request
            update_data['startDate'] = request.startDate.replace(tzinfo=timezone.utc)
            update_data['endDate'] = request.endDate.replace(tzinfo=timezone.utc)
        else:
            update_data = request.dict(exclude_unset=True)
            update_data['startDate'] = request.startDate.replace(tzinfo=timezone.utc)
            update_data['endDate'] = request.endDate.replace(tzinfo=timezone.utc)

        return await super().update(db, db_obj=db_obj, request=update_data)


booking_transport = CRUDBookingTransport(BookingTransport)
