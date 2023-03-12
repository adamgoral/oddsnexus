from abc import ABC
from dataclasses import field
from enum import Enum
from functools import singledispatchmethod
from typing import List

from oddsnexus.domain.common import Aggregate, DateTime, Entity, UniqueId, eventgeneratingmethod, valueobject, domainobject
from oddsnexus.domain.common import get_filtered_kwargs_for_type


Status = str
Team = str
Runner = str
Goals = int


class Status(Enum):
    SCHEDULED = 'scheduled'
    COMPLETED = 'completed'
    IN_PROGRESS = 'in_progress'
    CANCELLED = 'cancelled'


class Source(Enum):
    BETFAIR = 'betfair'
    

class Venue(Aggregate, ABC):
    id: UniqueId

class RaceTrack(Venue):
    ...

@valueobject
class Result():
    ...


@valueobject
class SourceId:
    source: Source
    id: str


@domainobject
class SportsEvent(Aggregate, ABC):
    start: DateTime
    status: Status = field(default=Status.SCHEDULED)
    venue_id: UniqueId
    result: Result = field(default=None)

    class ResultUpdated(Entity.Event):
        result: Result

    class StatusUpdated(Entity.Event):
        status: Status

    @valueobject
    class Created(Entity.Event):
        start: DateTime
        venue_id: UniqueId

    @valueobject
    class Observed(Entity.Event):
        start: DateTime
        venue_id: UniqueId
        source_id: SourceId
        status: Status = field(default=Status.SCHEDULED)
        

    @eventgeneratingmethod(ResultUpdated)
    def update_result(self, result: Result):
        self.result = result
        self.update_status(Status.COMPLETED)

    @eventgeneratingmethod(StatusUpdated)
    def update_status(self, status: Status):
        self.status = status

    @singledispatchmethod
    def _apply(self, event: 'Entity.Event'):
        return super().apply(event)

    @_apply.register(ResultUpdated)
    def _(self, event: 'SportsEvent.ResultUpdated'):
        self.result = event.result
        
    @_apply.register(StatusUpdated)
    def _(self, event: 'SportsEvent.StatusUpdated'):
        self.status = event.status


@valueobject
class SoccerScores():
    home: Goals
    away: Goals

@valueobject
class SoccerMatchResult(Result):
    first_half: SoccerScores
    second_half: SoccerScores

@valueobject
class HorseRaceResult(Result):
    finishers: List[Runner]


@domainobject
class SoccerMatch(SportsEvent):
    home: Team
    away: Team

    @valueobject
    class Created(SportsEvent.Created):
        home: Team
        away: Team

    @valueobject
    class Observed(SportsEvent.Observed):
        home: Team
        away: Team
        result: SoccerMatchResult = field(default=None)
        
    # @eventgeneratingmethod(Created)
    # def __init__(self, home: Team, away: Team, *args, **kwargs) -> 'SoccerMatch':
    #     self.home = home
    #     self.away = away
    #     super().__init__(*args, **kwargs)
        
    @classmethod
    def from_event(cls, event: 'SoccerMatch.Created'):
        kwargs = get_filtered_kwargs_for_type(SoccerMatch, **event.__dict__)
        result = SoccerMatch(**kwargs)
        return result

    @singledispatchmethod
    def _apply(self, event: 'Entity.Event'):
        return super().apply(event)


class HorseRace(SportsEvent):
    venue: RaceTrack
    runners: List[Runner]
    result: HorseRaceResult
