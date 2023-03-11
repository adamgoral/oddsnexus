import pytest

from oddsnexus.domain.common import DateTime
from oddsnexus.domain.sports import SoccerMatch, SoccerMatchResult, SoccerScores, Status
from oddsnexus.domain.common import Timestamp
from oddsnexus.domain.common import UniqueId


@pytest.mark.asyncio
async def test_create_from_event():
    created = SoccerMatch.Created(timestamp=Timestamp.create(),
                                  entity_id=UniqueId.create(),
                                  start=DateTime.today(),
                                  venue_id='abc',
                                  home='team1',
                                  away='team')
    actual = SoccerMatch.from_event(created)
    assert actual.start == created.start
    assert actual.venue_id == created.venue_id
    assert actual.home == created.home
    assert actual.away == created.away
    assert actual.status == Status.SCHEDULED
    assert actual.result is None
