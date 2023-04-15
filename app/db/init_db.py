from sqlalchemy.ext.asyncio import AsyncSession
from app import crud
from app.modules.organization.schema import OrganizationCreate
from app.modules.user.schema import UserUpdate
from app.db import base  # noqa: F401

async def init_db(db:AsyncSession) -> None:
    
    organization = await crud.organization.get_by_torid(
        db, id=400
    )
    if not organization:
        organization_in = OrganizationCreate(
            id=400,
            title="Гроднеское агенство",
            fullname="Гроднеское агенство"
        )
        await crud.organization.create(db, request=organization_in)
        print("***Success creating organization default.")
    else:
        print("Skipping creating organization.")

    org_def = await crud.organization.get_by_torid(
        db, id=400
    )

    user = await crud.user.get_by_username(db, username="admin")
    if not user:
        user_in = UserUpdate(
            username="admin",
            last_name="admin (default)",
            first_name="a",
            patronymic="",
            password="admin",
            is_superuser=True,
            is_active=True,
            organization_id=org_def.id,
        )
        await crud.user.create(db, request=user_in)
        print("***Success creating superuser default.")
    else:
        print("Skipping creating superuser.")

    #     logger.warning(
    #         "Skipping creating superuser. User with email "
    #         f"{settings.FIRST_SUPERUSER} already exists. "
    #     )
