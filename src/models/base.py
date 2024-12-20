import datetime
import uuid

from sqlalchemy import UUID, MetaData
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, declarative_base, mapped_column
from sqlalchemy.sql.functions import func
from typing_extensions import Annotated

int_pk = Annotated[int, mapped_column(primary_key=True)]

metadata = MetaData(schema="users")
base = declarative_base(metadata=metadata)


class Base(AsyncAttrs, base):
    __abstract__ = True


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class UUIDMixin:
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)