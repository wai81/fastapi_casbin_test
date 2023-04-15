from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
from fastapi_pagination import paginate, Page
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api.depend import get_db, get_current_user

from app.modules.order.schema import OrderCreate, Order, OrderInDB
from app.modules.user.schema import User

router = APIRouter()


@router.get("/all", status_code=200,
            response_model=Page[OrderInDB]
            # response_model=OrdersInDB
            # response_model=List[OrderInDB]
            )
async def all_orders(
        *,
        db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Cписок заказов
    """
    objects = await crud.order.get_all(db=db)

    # result = OrdersInDB(
    #     items=objects,
    #     total=len(objects)
    # )
    result = paginate(objects)
    return result


@router.get("/user-orders", status_code=200,
            # response_model=OrdersInDB
            response_model=Page[OrderInDB]
            )
async def orders_user(
        *,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
) -> Any:
    """
    Cписок заказов пользователя
    """

    # objects = await crud.order.get_all(db=db)
    objects = current_user.orders
    # objects = crud.order.get_orders(db=db)
    # result = OrdersInDB(
    #     orders=objects,
    #     ordersCount=len(objects)
    # )
    result = paginate(objects)
    return result


@router.get("/{order_id}", status_code=200, response_model=Order)
async def get_order(
        *,
        order_id: UUID,
        db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Заказ по id
    """
    obj = await crud.order.get(db=db, id=order_id)
    return obj


@router.post("/", status_code=201, response_model=Order)
async def create_order(
        *,
        request: OrderCreate,
        db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Новый заказ
    """
    new_obj = await crud.order.create(db=db, request=request)
    return new_obj


@router.delete("/{order_id}", status_code=200)
async def delete_order(
        *,
        order_id: UUID,
        db: AsyncSession = Depends(get_db)
):
    """
    Delete order
    """
    obj = await crud.order.get(db=db, id=order_id)
    if not obj:
        raise HTTPException(
            status_code=400, detail=f"Item with ID: {order_id} not found."
        )
    return await crud.order.remove(db=db, db_obj=obj)
