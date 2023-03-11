from abc import ABC, abstractmethod
from dataclasses import dataclass
import datetime as dt
from typing import List, Type
import uuid


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


class Message(ABC):
    timestamp: Timestamp


class Entity(ABC):
    unique_id: ID
    
    events: List['Entity.Event']

    def __init__(self) -> 'Entity':
        self.unique_id = UniqueId.create()
        self.events = list()

    def collect_events(self):
        result = self.events
        self.events = []
        return result

    class Event(Message, ABC):
        entity_id: ID

    class Command(Message, ABC):
        ...

class Aggregate(Entity, ABC):
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
