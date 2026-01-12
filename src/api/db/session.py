import sqlmodel
from sqlmodel import create_engine, SQLModel, Session
from .config import DATABASE_URL, DB_TIMEZONE
import timescaledb

if DATABASE_URL == "":
    raise NotImplementedError("DATABASE_URL need to be set")

engine = timescaledb.create_engine(DATABASE_URL, timezone=DB_TIMEZONE)


def init_db() -> None:
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("Creating hypertables...")
    timescaledb.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
