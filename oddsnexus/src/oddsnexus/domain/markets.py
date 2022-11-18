import datetime as dt
from typing import Dict, List

import faust

Price = int
Volume = int
ID = str
DateTime = dt.datetime
EventStatus = str
Team = str
SportsEventStatus = str
RaceTrack = str
Runner = str
Goals = int

class SportsEventOutcome(faust.Record):
    ...

class SoccerScores(faust.Record):
    home: Goals
    away: Goals

class SoccerMatchOutcome(SportsEventOutcome):
    first_half: SoccerScores
    second_half: SoccerScores

class HorseRaceOutcome(SportsEventOutcome):
    finishers: List[Runner]

class SportsEvent(faust.Record):
    id: ID
    start: DateTime
    status: SportsEventStatus
    outcome: SportsEventOutcome

class Event(faust.Record):
    id: ID
    status: EventStatus 

class SoccerMatch(SportsEvent):
    home: Team
    away: Team
    outcome: SoccerMatchOutcome

class HorseRace(SportsEvent):
    track: RaceTrack
    runners: List[Runner]
    outcome: HorseRaceOutcome

class HorseRaceWinner(Event):
    runner: Runner

class OrderBook(faust.Record):
    event_id: ID
    bids: Dict[Price, Volume]
    offers: Dict[Price, Volume]
