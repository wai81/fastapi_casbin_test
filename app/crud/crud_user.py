from typing import Optional, Union, Dict, Any, List

# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy import column, or_, text, desc, asc
from app.core.security import get_password_hash
from app.crud.base import CRUDBase
from app.modules.organization.model import Organization
from app.modules.user.model import User
from app.modules.user.schema import UserCreate, UserUpdate
from app.modules.user.filter import UserFilter


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    # def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
    #     return db.query(User).filter(User.email == email).first()

    async def get_all(
            self, db: AsyncSession, *,
            sort: str = None,
            order: str = None,
            filters: str = None,
    ) -> List[User]:
        # query = select(User). \
        #     options(joinedload('organization'))

        query = select(User).join(Organization)

        # if columns is not None and columns != "all":
        #     query = select(from_obj=self.model, columns=self.convert_columns(columns))

        if filters is not None and filters != "null":
            # we need filter format data like this  --> {'name': 'an','country':'an'}
            # convert string to dict format

            criteria = dict(x.split("*") for x in filters.split('-'))
            criteria_list = []

            # check every key in dict. are there any table attributes that are the same as the dict key ?
            for attr, value in criteria.items():
                _attr = getattr(self.model, attr)

                # filter format
                search = "%{}%".format(value)

                # criteria list
                criteria_list.append(_attr.like(search))

            query = query.filter(or_(*criteria_list))

        if sort is not None and sort != "null":
            if sort == '"organization.name"':
                sort = "name"
            # we need sort format data like this --> ['id','name']
            # if order is not None and order != "null":
            if order == '"desc"':
                query = query.order_by(desc(text(self.convert_sort(sort))))
            else:
                query = query.order_by(asc(text(self.convert_sort(sort))))
            # query = query.order_by(text(self.convert_sort(sort)))

        result = await db.execute(query)
        return result.scalars().all()

    async def get_users_filter(self, db: AsyncSession, *, filters: UserFilter):
        query = select(User).join(Organization)
        query = filters.filter(query)
        query = filters.sort(query)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_by_username(self, db: AsyncSession, *, username: str) -> Optional[User]:
        query = select(User).where(User.username == username)
        result = await db.execute(query)
        obj = result.scalars().first()
        return obj

    async def create(self, db: AsyncSession, *, request: UserCreate) -> User:
        create_data = request.dict()
        create_data.pop("password")
        obj = User(**create_data)
        obj.hashed_password = get_password_hash(request.password)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def update(self, db: AsyncSession, *, db_obj: User, request: Union[UserUpdate, Dict[str, Any]]) -> User:
        if isinstance(request, dict):
            update_data = request
        else:
            update_data = request.dict(exclude_unset=True)

        return await super().update(db, db_obj=db_obj, request=update_data)

    async def add_access_tor(self, db: AsyncSession, *, db_obj: User, tor_ids: List[int]) -> User:
        obj = await self.get(db=db, id=db_obj.id)
        for tor_id in tor_ids:
            tor = await db.get(Organization, tor_id)
            obj.access_tors.append(tor)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def remove_access_tor(self, db: AsyncSession, *, db_obj: User, tor_ids: List[int]) -> User:
        obj = await self.get(db=db, id=db_obj.id)
        for tor_id in tor_ids:
            tor = await db.get(Organization, tor_id)
            obj.access_tors.remove(tor)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def is_superuser(self, user: User) -> bool:
        return user.is_superuser

    def convert_sort(self, sort):
        """
        # separate string using split('-')
        split_sort = sort.split('-')
        # join to list with ','
        new_sort = ','.join(split_sort)
        """
        return ','.join(sort.split('-'))

    def convert_columns(self, columns):
        """
        # seperate string using split ('-')
        new_columns = columns.split('-')
        # add to list with column format
        column_list = []
        for data in new_columns:
            column_list.append(data)
        # we use lambda function to make code simple
        """

        return list(map(lambda x: column(x), columns.split('-')))


user = CRUDUser(User)
