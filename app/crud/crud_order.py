import datetime
from typing import List


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from app.core.sequences import create_order_no
from app.crud.base import CRUDBase
from app.modules.order.model import Order
from app.modules.order.schema import OrderCreate, OrderUpdate


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):

    async def get(self, db: AsyncSession, id: str) -> Order:
        query = select(Order). \
            where(Order.id == id).\
            options(joinedload('organization')).\
            options(joinedload('order_creator'))
        result = await db.execute(query)
        return result.scalars().first()

    async def get_all(self, db: AsyncSession, ) -> List[Order]:
        query = select(Order). \
            options(joinedload('organization')).\
            options(joinedload('order_creator'))
        result = await db.execute(query)
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, request: OrderCreate) -> Order:
        order_no = await create_order_no(
            db=db,
            day=datetime.date.today(),
            tor_id=request.organization_id,
        )
        create_data = request.dict()
        obj = Order(**create_data)
        obj.order_no = order_no

        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj


order = CRUDOrder(Order)
