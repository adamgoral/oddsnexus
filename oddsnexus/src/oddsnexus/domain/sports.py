from enum import Enum
from dataclasses import dataclass
from typing import List
import faust

from oddsnexus.domain.common import Aggregate, DateTime, Entity, ID, valueobject


Status = str
Team = str
Runner = str
Goals = int


class Status(Enum):
    SCHEDULED = 'scheduled'
    COMPLETED = 'completed'
    IN_PROGRESS = 'in_progress'
    CANCELLED = 'cancelled'


class Venue(Aggregate, abstract=True):
    id: ID

class RaceTrack(Venue):
    ...

@valueobject
class Result():
    ...

class Event(Aggregate, abstract=True):
    id: ID
    start: DateTime
    status: Status
    venue_id: ID
    result: Result

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

class SoccerMatch(Event):
    home: Team
    away: Team
    result: SoccerMatchResult

class HorseRace(Event):
    venue: RaceTrack
    runners: List[Runner]
    result: HorseRaceResult
