from oddsnexus.domain import sports

import faust

app = faust.App(__name__, broker='kafka://kafka:9092')

sport_event_topic = app.topic('sport_event', key_type=str, value_type=sports.Event)

@app.timer(interval=1.0)
async def discover_markets(app):
    sport_event: sports.SoccerMatch = sports.SoccerMatch.create()
    sport_event_topic.send(key=sport_event.id, value=sport_event)