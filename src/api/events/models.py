# from pydantic import BaseModel, Field
from typing import List, Optional
from sqlmodel import SQLModel, Field, DateTime
from datetime import datetime, timezone
from timescaledb import TimescaleModel
from timescaledb.utils import get_utc_now


# def get_utc_now() -> datetime:
#     return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)

# page visits at any given time


class EventModel(TimescaleModel, table=True):

    # id: Optional[int] = Field(default=None, primary_key=True)
    page: str = Field(index=True)  # /about, /contact ...
    description: Optional[str] = ""
    # created_at: datetime = Field(
    #     default_factory=get_utc_now,
    #     sa_type=DateTime(timezone=True),
    #     nullable=False,
    # )
    updated_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=DateTime(timezone=True),
        nullable=False,
    )

    __chunk_time_interval__ = "INTERVAL 1 day"
    __drop_after__ = "INTERVAL 3 months"


class EventListSchema(SQLModel):

    results: List[EventModel]
    count: int


class EventCreateSchema(SQLModel):

    page: str
    description: Optional[str] = Field(default="my description")


class EventUpdateSchema(SQLModel):

    description: str
