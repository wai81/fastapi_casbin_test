import datetime

from typing import List

from fastapi import Depends, APIRouter, HTTPException, Query

from sqlalchemy import cast, Date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app import crud
from app.api.depend import get_db
from app.modules.receipt.model import Receipt
from app.modules.receipt.schema import ReceiptCreateInDB, ReceiptInDB

router = APIRouter()


@router.post("/receipt/", status_code=201, response_model=ReceiptInDB)
async def create_receipt(*, receipt_in: ReceiptCreateInDB, db: AsyncSession = Depends(get_db)) -> dict:
    """
    Новая квитанция из 1С

    """
    receipt = await crud.receipt.find_by_number(db=db, number=receipt_in.personal_account)
    if receipt is not None:
        upd_obj = await crud.receipt.update(db=db, db_obj=receipt, request=receipt_in)
        return upd_obj
    else:
        new_obj = await crud.receipt.create_receipt_from_request(db=db, obj_in=receipt_in)
        return new_obj


@router.get("/receipts_paid/", status_code=201, response_model=List[ReceiptInDB])
async def get_receipts_paid(*,
                      number_receipt: str = Query(None,
                                                  description='Номер квитанциии'),
                      date_receipt: datetime.date = Query(None,
                                                          description='Дата квитанциии'),
                      db: AsyncSession = Depends(get_db)) -> dict:
    """
    Получить квитанции
    """

    # query = db.query(Receipt)
    # query = query.filter(Receipt.status == 2)
    query = select(Receipt).where(Receipt.status == 2,)
    if number_receipt:
        query = query.where(Receipt.personal_account == number_receipt)

    if date_receipt:
        query = query.where(cast(Receipt.created_at, Date) == date_receipt)

    #obj = query.all() #crud.receipt.find_only_payed(db=db)
    result = await db.execute(query)
    obj = result.scalars().all()
    if not obj:
        raise HTTPException(
            status_code=400, detail=f"Objects with not found."
        )

    return obj

