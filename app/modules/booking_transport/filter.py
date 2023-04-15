from datetime import datetime
from typing import Optional, List

from fastapi_filter import FilterDepends, with_prefix
from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field
from pydantic.types import UUID4

from app.modules.booking_transport.model import Transport, BookingTransport
from app.modules.organization.filter import OrganizationFilter
from app.modules.subunit.filter import SubunitFilter


class TransportFilter(Filter):
    q: Optional[str]
    id__in: Optional[List[UUID4]]

    class Constants(Filter.Constants):
        model = Transport
        search_field_name = "q"
        search_model_fields = ["title"]


class BookingTransportListFilter(Filter):
    order_by: Optional[list[str]]
    q: Optional[str]
    title: Optional[str]
    title__like: Optional[str] = Field(alias='title_like')
    startDate__gte: Optional[datetime] = Field(alias='startDate_gte')
    startDate__lte: Optional[datetime] = Field(alias='startDate_lte')
    is_active: Optional[bool]
    subunit: Optional[SubunitFilter] = FilterDepends(with_prefix('subunit', SubunitFilter))
    transport: Optional[TransportFilter] = FilterDepends(with_prefix('transport', TransportFilter))
    organization: Optional[OrganizationFilter] = FilterDepends(with_prefix('organization', OrganizationFilter))

    class Constants(Filter.Constants):
        model = BookingTransport
        search_field_name = 'q'
        search_model_fields = ["title"]

    class Config:
        allow_population_by_field_name = True


class TransportListFilter(Filter):
    order_by: Optional[list[str]]
    q: Optional[str]
    title: Optional[str]
    title__like: Optional[str] = Field(alias='title_like')
    is_active: Optional[bool]

    class Constants(Filter.Constants):
        model = Transport
        search_field_name = 'q'
        search_model_fields = ["title"]

    class Config:
        allow_population_by_field_name = True
