from typing import Optional

from fastapi_filter import FilterDepends, with_prefix
from fastapi_filter.contrib.sqlalchemy import Filter

from app.modules.organization.filter import OrganizationFilter
from app.modules.user.model import User


class UserFilter(Filter):
    order_by: Optional[list[str]]
    q: Optional[str]
    organization: Optional[OrganizationFilter] = FilterDepends(with_prefix('organization', OrganizationFilter))

    class Constants(Filter.Constants):
        model = User
        search_field_name = 'q'
        search_model_fields = ["last_name", "first_name", "patronymic", "username"]
