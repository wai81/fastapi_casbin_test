from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud
from app.api.depend import get_db
from app.modules.receipt.schema import ReceiptCreate, ReceiptInDB, ReceiptUpdate, ReceiptsInDB

router = APIRouter()


@router.get("/", status_code=200, response_model=ReceiptsInDB)
async def receipts(
        *,
        db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Cписок квитанций для оплаты
    """
    objects = await crud.receipt.get_all(db=db)
    result = ReceiptsInDB(
        receipts=objects,
        receiptsCount=len(objects)
    )
    return result


@router.get("/{receipt_id}", status_code=200, response_model=ReceiptInDB)
async def get_receipt(
        *,
        receipt_id: UUID,
        db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Квитанция для оплаты по id
    """
    obj = await crud.receipt.get(db=db, id=receipt_id)
    return obj


@router.post("/", status_code=201, response_model=ReceiptInDB)
async def create_receipt(
        *,
        request: ReceiptCreate,
        db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Новая квитанция для оплаты
    """
    new_obj = await crud.receipt.create(db=db, request=request)
    return new_obj


@router.put("/{receipt_id}", status_code=201, response_model=ReceiptInDB)
async def update_receipt(
        *,
        receipt_id: UUID,
        request: ReceiptUpdate,
        db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Изменить квитанцию для оплаты
    """
    receipt = await crud.receipt.get(db=db, id=receipt_id)
    if not receipt:
        raise HTTPException(
            status_code=400, detail=f"Recipe with ID: {receipt_id} not found."
        )
    upd_obj = await crud.receipt.update(db=db, db_obj=receipt, request=request)
    return upd_obj


@router.delete("/{receipt_id}", status_code=200)
async def delete_receipt(
        *,
        receipt_id: UUID,
        db: AsyncSession = Depends(get_db)
):
    """
    Удалить квитанцию для оплаты
    """
    obj = await crud.receipt.get(db=db, id=receipt_id)
    if not obj:
        raise HTTPException(
            status_code=400, detail=f"Item with ID: {receipt_id} not found."
        )
    return await crud.receipt.remove(db=db, db_obj=obj)




