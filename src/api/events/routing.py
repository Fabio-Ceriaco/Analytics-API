from fastapi import APIRouter, Depends, HTTPException, Query
from .models import (
    EventBucketSchema,
    EventModel,
    EventListSchema,
    EventCreateSchema,
    get_utc_now,
)
from typing import List
from timescaledb.hyperfunctions import time_bucket, time_bucket_gapfill
from datetime import datetime, timedelta, timezone
from sqlalchemy import case, func
from api.db.session import get_session
from sqlmodel import Session, desc, select


router = APIRouter()

DEFAULT_LOOKUP_PAGES = [
    "/",
    "/about",
    "/pricing",
    "/contact",
    "/blog",
    "/products",
    "/login",
    "/signup",
    "/dashboard",
    "/settings",
]


@router.get("/", response_model=List[EventBucketSchema])
def read_events(
    duration: str = "1 day",
    pages: List = Query(default=None),
    session: Session = Depends(get_session),
):
    # a bunch of items in a table
    os_case = case(
        (EventModel.user_agent.ilike("%Windows%"), "Windows"),
        (EventModel.user_agent.ilike("%Macintosh%"), "MacOS"),
        (EventModel.user_agent.ilike("%Linux%"), "Linux"),
        (EventModel.user_agent.ilike("%iphone%"), "iOS"),
        (EventModel.user_agent.ilike("%android%"), "Android"),
        else_="Other",
    ).label("operating_system")
    bucket = time_bucket("1 day", EventModel.time)
    lookup_pages = (
        pages if isinstance(pages, list) and len(pages) > 0 else DEFAULT_LOOKUP_PAGES
    )
    query = (
        select(
            bucket.label("bucket"),
            os_case,
            EventModel.user_agent.label("user_agent"),
            EventModel.page.label("page"),
            func.avg(EventModel.duration).label("avg_duration"),
            func.count().label("count"),
        )
        .where(
            EventModel.page.in_(lookup_pages),
        )
        .group_by(bucket, EventModel.user_agent, os_case, EventModel.page)
        .order_by(bucket.asc(), os_case.asc(), EventModel.page.asc())
    )
    results = session.exec(query).fetchall()
    return results


@router.post("/", response_model=EventModel)
def create_event(payload: EventCreateSchema, session: Session = Depends(get_session)):
    # a bunch of items in a table
    print(payload.page)
    data = payload.model_dump()  # payload -> dict -> pydantic
    obj = EventModel.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


@router.get("/{event_id}", response_model=EventModel)
def get_event(event_id: int, session: Session = Depends(get_session)):
    # single row
    query = select(EventModel).where(EventModel.id == event_id)
    result = session.exec(query).first()
    if not result:
        raise HTTPException(status_code=404, detail="Event not found")
    return result
