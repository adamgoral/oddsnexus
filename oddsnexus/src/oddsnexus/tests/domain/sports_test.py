import faust

from oddsnexus.domain.common import DateTime
from oddsnexus.domain.sports import SoccerMatch, SoccerMatchResult, SoccerScores, Status

async def test_dump():
    expected = SoccerMatch(
        id='123',
        start=DateTime.today(),
        status=Status.SCHEDULED,
        venue_id='abc',
        home='team1',
        away='team',
        result=SoccerMatchResult(
            first_half=SoccerScores(
                home=0,
                away=0
            ),
            second_half=SoccerScores(
                home=1,
                away=0
            )
        )
    )

    actual = SoccerMatch.loads(expected.dumps())
    assert expected == actual