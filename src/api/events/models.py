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

    page: str = Field(index=True)  # /about, /contact ...
    user_agent: Optional[str] = Field(default="", index=True)  # browser info
    ip_address: Optional[str] = Field(default="", index=True)  # user IP
    referrer: Optional[str] = Field(default="", index=True)  # where they came from
    session_id: Optional[str] = Field(index=True)  # track user sessions
    duration: Optional[int] = Field(default=0)  # in seconds

    __chunk_time_interval__ = "INTERVAL 1 day"
    __drop_after__ = "INTERVAL 3 months"


class EventListSchema(SQLModel):

    results: List[EventModel]
    count: int


class EventCreateSchema(SQLModel):

    page: str
    user_agent: Optional[str] = Field(default="", index=True)  # browser info
    ip_address: Optional[str] = Field(default="", index=True)  # user IP
    referrer: Optional[str] = Field(default="", index=True)  # where they came from
    session_id: Optional[str] = Field(index=True)  # track user sessions
    duration: Optional[int] = Field(default=0)  # in seconds


class EventBucketSchema(SQLModel):

    bucket: datetime
    page: str
    user_agent: Optional[str] = ""
    operating_system: Optional[str] = ""
    avg_duration: Optional[float] = 0.0
    count: int
