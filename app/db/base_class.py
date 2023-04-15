from datetime import datetime, timezone
from typing import Any

from sqlalchemy import Column, DateTime, TIMESTAMP, func
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str
    # created_at = Column(DateTime, default=datetime.now(timezone.utc))
    # created_at = Column(DateTime, server_default=func.now())
    created_at = Column(type_=TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))


    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
