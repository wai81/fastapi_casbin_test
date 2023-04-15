from typing import Optional, List

from fastapi import Query
from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field

from app.modules.organization.model import Organization


class OrganizationFilter(Filter):
    q: Optional[str]
    id__in: Optional[List[int]]

    class Constants(Filter.Constants):
        model = Organization
        search_field_name = "q"
        search_model_fields = ["title"]

    # class Config:
    #     allow_population_by_field_name = True


class OrganizationListFilter(Filter):
    order_by: Optional[list[str]]
    q: Optional[str]
    id: Optional[int]
    id__neq: Optional[int] = Field(alias='id_ne')
    id__gte: Optional[int] = Field(alias='id_gte')
    id__lte: Optional[int] = Field(alias='id_lte')

    title: Optional[str]
    title__like: Optional[str] = Field(alias='title_like')

    class Constants(Filter.Constants):
        model = Organization
        search_field_name = "q"
        search_model_fields = ["title"]

    class Config:
        allow_population_by_field_name = True

