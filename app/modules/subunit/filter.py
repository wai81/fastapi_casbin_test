from typing import Optional, List


from fastapi_filter import FilterDepends, with_prefix
from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field
from pydantic.types import UUID4
from app.modules.organization.filter import OrganizationFilter
from app.modules.subunit.model import Subunit


class SubunitFilter(Filter):
    q: Optional[str]
    id__in: Optional[List[UUID4]]

    class Constants(Filter.Constants):
        model = Subunit
        search_field_name = "q"
        search_model_fields = ["title"]


class SubunitListFilter(Filter):
    order_by: Optional[list[str]]
    q: Optional[str]
    title: Optional[str]
    title__like: Optional[str] = Field(alias='title_like')
    is_active: Optional[bool]
    organization: Optional[OrganizationFilter] = FilterDepends(with_prefix('organization', OrganizationFilter))

    class Constants(Filter.Constants):
        model = Subunit
        search_field_name = 'q'
        search_model_fields = ["name"]

    class Config:
        allow_population_by_field_name = True
