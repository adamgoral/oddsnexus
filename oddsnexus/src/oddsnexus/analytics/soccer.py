
from enum import Enum

from oddsnexus.analytics.common import Event, valueobject


class SoccerWinningTeam(Enum):
    HOME = 'home'
    AWAY = 'away'
    DRAW = 'draw'


class MatchStage(Enum):
    FIRST_HALF = 'first_half'
    SECOND_HALF = 'second_half'
    FINAL = 'final'


@valueobject
class SoccerMatchWinner(Event):
    match_stage: MatchStage
    team: SoccerWinningTeam
