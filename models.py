from pydantic import BaseModel
from datetime import date, time

class Event(BaseModel):
    name: str
    date: date
    start: time
    end: time
