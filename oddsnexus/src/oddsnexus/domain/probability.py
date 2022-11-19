from enum import Enum
import faust

from oddsnexus.domain.common import ID

class SoccerWinningTeam(Enum):
    HOME = 'home'
    AWAY = 'away'
    DRAW = 'draw'

class MatchStage(Enum):
    FIRST_HALF = 'first_half'
    SECOND_HALF = 'second_half'
    FINAL = 'final'

class Event(faust.Record):
    id: ID
    sports_event_id: ID

class SoccerMatchWinner(Event):
    match_stage: MatchStage
    team: SoccerWinningTeam

class HorseRaceWinner(Event):
    runner_id: ID