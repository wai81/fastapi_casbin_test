from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api.depend import get_db
from app.modules.receipt.schema import Receipt, ReceiptUpdateStatus, ReceiptInDB

router = APIRouter()


@router.get("/{number}", status_code=200, response_model=Receipt)
def get_receipt(
        *,
        number: str,
        db: Session = Depends(get_db),
) -> dict:
    """
    Квитанция для оплаты по номеру квитанции
    """
    obj = crud.receipt.find_by_number(db=db, number=number)
    if not obj:
        raise HTTPException(
            status_code=400, detail=f"Recipe with number: {number} not found."
        )

    return obj


@router.put("/{number}", status_code=201, response_model=ReceiptInDB)
def change_status_receipt(
        *,
        number: str,
        request: ReceiptUpdateStatus,
        db: Session = Depends(get_db)
) -> dict:
    """
    Изменить квитанцию для оплаты
    """
    obj = crud.receipt.find_by_number(db=db, number=number)
    if not obj:
        raise HTTPException(
            status_code=400, detail=f"Recipe with number: {number} not found."
        )
    upd_obj = crud.receipt.update(db=db, db_obj=obj, request=request)
    return upd_obj
