from enum import Enum
from typing import List
import faust

from oddsnexus.domain.common import Entity, DateTime, ID


Status = str
Team = str
Runner = str
Goals = int


class Status(Enum):
    SCHEDULED = 'scheduled'
    COMPLETED = 'completed'
    IN_PROGRESS = 'in_progress'
    CANCELLED = 'cancelled'


class Venue(Entity, abstract=True):
    id: ID

class RaceTrack(Venue):
    ...

class Result(Entity, abstract=True):
    ...

class Event(Entity, abstract=True):
    id: ID
    start: DateTime
    status: Status
    venue: Venue
    result: Result

class SoccerScores():
    home: Goals
    away: Goals

class SoccerMatchResult(Result):
    first_half: SoccerScores
    second_half: SoccerScores

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
