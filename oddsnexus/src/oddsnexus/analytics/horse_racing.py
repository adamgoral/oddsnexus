from oddsnexus.analytics.common import Event
from oddsnexus.domain.common import ID


class HorseRaceWinner(Event):
    runner_id: ID
