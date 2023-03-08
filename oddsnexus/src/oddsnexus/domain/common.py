from dataclasses import dataclass
import datetime as dt
from typing import List, Type
import uuid

import faust


ID = str
DateTime = dt.datetime

valueobject = dataclass(frozen=True, eq=True)

@valueobject
class Timestamp:
    utc: dt.datetime

    @staticmethod
    def create() -> 'Timestamp':
        return Timestamp(dt.datetime.utcnow())

@valueobject
class UniqueId:
    guid: uuid.UUID

    @staticmethod
    def create() -> 'UniqueId':
        return UniqueId(uuid.uuid4())

class Message(faust.Record, abstract=True):
    timestamp: Timestamp

class Entity(faust.Record, abstract=True):
    unique_id: ID
    
    events: List['Entity.Event'] = faust.models.fields.FieldDescriptor(exclude=True)

    def __init__(self) -> 'Entity':
        self.unique_id = UniqueId.create()
        self.events = list()

    def collect_events(self):
        result = self.events
        self.events = []
        return result

    class Event(Message, abstract=True):
        entity_id: ID

    class Command(Message, abstract=True):
        ...

class Aggregate(Entity, abstract=True):
    ...

def eventgeneratingmethod(event_type: Type):
    
    def inner(func):

        def wrapper(self: Entity, *args, **kwargs):
            if not issubclass(event_type, Entity.Event):
                raise ValueError(f'event_type must subclass of Entity.Event')
            func(self, *args, **kwargs)
            self.events.append(event_type(Timestamp.create(), self.id, *args, **kwargs))
        return wrapper

    return inner