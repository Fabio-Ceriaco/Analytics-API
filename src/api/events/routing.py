from fastapi import APIRouter
from .schemas import EventSchema, EventListSchema

router = APIRouter()


@router.get("/")
def read_events() -> EventListSchema:
    # a bunch of items in a table
    return {
        "results": [{"id": 1}, {"id": 2}, {"id": 3}],
        "count": 3,
    }


@router.post("/")
def create_event(data: dict = {}) -> EventSchema:
    # a bunch of items in a table
    print(type(data))
    return {"id": 123}


@router.get("/{event_id}")
def get_event(event_id: int) -> EventSchema:
    # single row
    return {"id": event_id}


@router.put("/{event_id}")
def get_event(event_id: int, payload: dict = {}) -> EventSchema:
    # single row
    return {"id": event_id}


# # @router.delete("/{event_id}")
# def get_event(event_id: int, payload: dict = {}) -> EventSchema:
#     # single row
#     return {"id": event_id}
