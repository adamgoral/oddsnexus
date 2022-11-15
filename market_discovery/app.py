import faust
import datetime as dt

class Market(faust.Record):
    timestamp: dt.datetime
    id: str
    description: str

app = faust.App('odds-nexus-markets-discovery', broker='kafka://kafka:9092')
markets = app.topic('markets', value_type=Market)

@app.timer(interval=1.0)
async def market(app):
    greeting = Market(timestamp=dt.datetime.now(), id='test', description='test description')
    await markets.send(
        value=greeting
    )
