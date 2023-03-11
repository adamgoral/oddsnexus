from abc import ABC
from enum import Enum
from dataclasses import dataclass
from typing import List

from oddsnexus.domain.common import Aggregate, DateTime, Entity, ID, UniqueId, eventgeneratingmethod, valueobject


Status = str
Team = str
Runner = str
Goals = int


class Status(Enum):
    SCHEDULED = 'scheduled'
    COMPLETED = 'completed'
    IN_PROGRESS = 'in_progress'
    CANCELLED = 'cancelled'


class Venue(Aggregate, ABC):
    id: ID

class RaceTrack(Venue):
    ...

@valueobject
class Result():
    ...

class Event(Aggregate, ABC):
    start: DateTime
    status: Status
    venue_id: UniqueId
    result: Result

    def __init__(self, start: DateTime, venue_id: ID) -> 'Event':
        super().__init__()
        self.start = start
        self.venue_id = venue_id
        self.status = Status.SCHEDULED
        self.result = None

    class ResultUpdated(Entity.Event):
        result: Result

    class StatusUpdated(Entity.Event):
        status: Status

    @eventgeneratingmethod(ResultUpdated)
    def update_result(self, result: Result):
        self.result = result
        self.update_status(Status.COMPLETED)

    @eventgeneratingmethod(StatusUpdated)
    def update_status(self, status: Status):
        self.status = status


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

@dataclass
class SoccerMatch(Event):
    home: Team
    away: Team
    result: SoccerMatchResult

    class Created(Entity.Event):
        home: Team
        away: Team

    @eventgeneratingmethod(Created)
    def __init__(self) -> 'SoccerMatch':
        super().__init__()


    def set_result(self, result: SoccerMatchResult):
        self.result = result


class HorseRace(Event):
    venue: RaceTrack
    runners: List[Runner]
    result: HorseRaceResult
