import datetime
from typing import TypeVar, Type

from sqlalchemy import func, cast, Date, extract
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.modules.order.model import Order
from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)


async def create_number(db: AsyncSession, model: Type[ModelType]):
    # count_item = await db.query(model).count()
    query = select(func.count()).select_from(select(model))

    result = await db.execute(query)
    count_item = result.scalar()

    next_item = count_item + 1
    day = datetime.date.today()

    y = day.strftime('%Y')
    m = day.strftime('%m')
    d = day.strftime('%d')
    new_number = y + m + d + "{:05d}".format(next_item)
    return new_number


async def create_number_day_by_tor(db: AsyncSession, day: datetime.date, tor_id: int, model: Type[ModelType]):
    # count_item = await db.query(model).filter_by(
    #     tor_id=tor_id).filter(cast(model.created_at, Date) == day).count()  # db.query(model).count()
    query = select(func.count()).select_from(select(model).where(
        model.tor_id == tor_id,
        cast(model.created_at, Date) == day,
    ))
    result = await db.execute(query)
    count_item = result.scalar()
    next_item = count_item + 1
    y = day.strftime('%Y')
    m = day.strftime('%m')
    d = day.strftime('%d')
    new_number = y + m + d + str(tor_id) + "{:05d}".format(next_item)
    return new_number


async def create_number_by_tor(db: AsyncSession, tor_id: int, model: Type[ModelType]):
    # count_item = await db.query(model).filter_by(tor_id=tor_id).count()  # db.query(model).count()
    query = select(func.count()).select_from(select(model).where(
        model.tor_id == tor_id,
    ))
    result = await db.execute(query)
    count_item = result.scalar()
    next_item = count_item + 1
    current_date = datetime.date.today()
    year = current_date.strftime('%Y')
    month = current_date.strftime('%m')
    day = current_date.strftime('%d')

    new_number = year + month + day + str(tor_id) + "{:05d}".format(next_item)
    return new_number


async def create_order_no(db: AsyncSession, day: datetime.date, tor_id: int, ):
# def create_order_no(db: Session, day: datetime.date, tor_id: int, ):
    query = select(func.count()).select_from(select(Order).where(
        Order.organization_id == tor_id,
        extract('year', Order.created_at) == day.year,
    ))
    result = await db.execute(query)
    count_orders = result.scalar()

    # count_orders = db.query(Order).filter_by(
    #      order_tor_id=tor_id).filter(extract('year', Order.created_at) == day.year).count()  # db.query(model).count()
    next_no = count_orders + 1
    year = day.strftime('%y')
    new_number = year + str(tor_id) + "{:05d}".format(next_no)
    print(f'number {new_number}')
    return new_number
