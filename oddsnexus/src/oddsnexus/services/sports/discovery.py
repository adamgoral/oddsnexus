import faust

app = faust.App(__name__, broker='kafka://kafka:9092')

@app.timer(interval=1.0)
async def discover_markets(app):
    ...
