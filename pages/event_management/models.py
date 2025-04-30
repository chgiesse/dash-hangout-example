from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import List, Tuple


class EventsQueryParams(BaseModel):
    search_value: str | int | None = None

    @property
    def ui_search_value(self):
        return self.search_value if self.search_value else ''
    
    @property
    def db_search_value(self):
        return None if self.search_value == '' else self.search_value

    @field_validator('search_value', mode='after')
    @classmethod
    def validate(cls, value):
        try:
            return int(value)
        except ValueError:
            return value


class EventFormModel(BaseModel):
    name: str
    location: str
    date: datetime


class EventsModel(BaseModel):
    id: int
    name: str
    location: str
    date: datetime
    participants: List[str | None]

    @classmethod
    def from_db(cls, events: List[Tuple[any]]) -> List['EventsModel']:
        event_models = []
        for event in events:
            event_models.append(cls(
                id=event[0],
                name=event[1],
                location=event[2],
                date=event[3],
                participants=event[4] 
            ))
        return event_models
    
    @classmethod
    def get_column_names(cls):
        return [name.title() for name in cls.__annotations__.keys()]
