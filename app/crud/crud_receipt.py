import datetime
from typing import List

# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.sequences import create_number_day_by_tor
from app.crud.base import CRUDBase
from app.modules.receipt.model import Receipt
from app.modules.receipt.schema import ReceiptCreate, ReceiptUpdate, ReceiptCreateInDB, ReceiptInDB


class CRUDReceipt(CRUDBase[Receipt, ReceiptCreate, ReceiptUpdate]):

    async def find_by_number(self, db: AsyncSession, *, number: str):
        # query = await db.query(Receipt)
        # return query.filter(Receipt.personal_account == number).first()
        query = select(Receipt).where(Receipt.personal_account == number)
        result = await db.execute(query)
        return result.scalars().first()

    async def find_by_order(self, db: AsyncSession, *, order: str):
        # query = await db.query(Receipt)
        # return query.filter(Receipt.order == order).first()
        query = select(Receipt).where(Receipt.order == order)
        result = await db.execute(query)
        return result.scalars().first()

    async def find_only_payed(self, db: AsyncSession) -> List[ReceiptInDB]:
        # query = await db.query(Receipt)
        # return query.filter(Receipt.status == 2).all()
        query = select(Receipt).where(Receipt.status == 2)
        result = await db.execute(query)
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, request: ReceiptCreate) -> Receipt:
        create_data = request.dict()
        obj = Receipt(**create_data)
        obj.personal_account = create_number_day_by_tor(
            db=db,
            day=datetime.date.today(),
            tor_id=request.tor_id,
            model=Receipt
        )
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def create_receipt_from_request(self, db: AsyncSession, *, obj_in: ReceiptCreateInDB) -> ReceiptInDB:
        create_data = obj_in.dict()
        obj = Receipt(**create_data)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj


receipt = CRUDReceipt(Receipt)
