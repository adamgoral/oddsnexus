from oddsnexus.analytics.common import Event
from oddsnexus.domain.common import UniqueId


class HorseRaceWinner(Event):
    runner_id: UniqueId
