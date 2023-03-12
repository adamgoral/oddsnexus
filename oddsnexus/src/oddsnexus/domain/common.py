from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import datetime as dt
import inspect
from typing import List, Type
import uuid


DateTime = dt.datetime

valueobject = dataclass(frozen=True, eq=True, kw_only=True)
domainobject = dataclass(kw_only=True)

class AggregateEventIdMismatch(Exception):
    aggregate_id: str
    event_id: str

    def __init__(self, aggregate_id: str, event_id: str) -> None:
        self.aggregate_id = aggregate_id
        self.event_id = event_id

@valueobject
class Timestamp:
    utc: dt.datetime

    @staticmethod
    def create() -> 'Timestamp':
        return Timestamp(utc=dt.datetime.utcnow())

@valueobject
class UniqueId:
    guid: uuid.UUID

    @staticmethod
    def create() -> 'UniqueId':
        return UniqueId(guid=uuid.uuid4())


@valueobject
class Message(ABC):
    timestamp: Timestamp = field(default_factory=Timestamp.create)


@domainobject
class Entity(ABC):
    unique_id: UniqueId = field(default_factory=UniqueId.create)

    @valueobject
    class Event(Message, ABC):
        entity_id: UniqueId

    class Command(Message, ABC):
        ...


@domainobject
class Aggregate(Entity, ABC):
    events: List['Entity.Event'] = field(default_factory=list, compare=False)

    @property
    def uncommited_events(self):
        return tuple(self._events)

    def mutate(self, event:'Entity.Event'):
        if self.id != event.id:
            raise AggregateEventIdMismatch(aggregate_id=self.id, event_id=event.id)
        self._apply(event)
        self._events.append(event)
        return self

    def _apply(self, e: 'Entity.Event'):
        raise NotImplementedError
    

def get_filtered_kwargs_for_type(cls: Type, **kwargs):
    params = inspect.signature(cls).parameters
    result = {
        k: v for k, v in kwargs.items() 
        if k in params
    }
    return result


def eventgeneratingmethod(event_type: Type):
    
    def inner(func):

        def wrapper(self: Entity, *args, **kwargs):
            if not issubclass(event_type, Entity.Event):
                raise ValueError(f'event_type must subclass of Entity.Event')
            entity_type_kwargs = get_filtered_kwargs_for_type(self.__class__, **kwargs)
            func(self, **entity_type_kwargs)
            event_type_kwargs = get_filtered_kwargs_for_type(event_type, **kwargs)
            event_type_kwargs['entity_id'] = self.unique_id
            self.events.append(event_type(**event_type_kwargs))
        return wrapper

    return inner
