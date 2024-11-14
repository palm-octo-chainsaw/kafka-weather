import os
from datetime import datetime
from typing import Annotated
from fastapi import Depends
from sqlalchemy import URL, create_engine
from sqlmodel import Field, Session, SQLModel


class Location(SQLModel, table=True):
    __tablename__ = 'location'
    location_id: int | None = Field(default=None, primary_key=True)
    latitude: float
    longitude: float
    generationtime_ms: float
    utc_offset_seconds: int
    timezone: str
    timezone_abbreviation: str
    elevation: int
    hourly_units: str


class Observations(SQLModel, table=True):
    __tablename__ = 'observations'
    observation_id: int | None = Field(default=None, primary_key=True)
    location: int = Field(foreign_key='location.location_id')
    time: datetime
    temperature_2m: float
    relative_humidity_2m: int


CONNECTION_STRING = URL.create(
    drivername=os.getenv('DB_DRIVER'),
    username=os.getenv('DB_USERNAME'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_DATABASE'),
)

CONNECTION_ARGS = {"check_same_thread": False}

engine = create_engine(CONNECTION_STRING, connect_args=CONNECTION_ARGS)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
