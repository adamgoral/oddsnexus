from typing import Dict, List

import faust

Price = int
Volume = int
ID = str
EventStatus = str

class Outcome(faust.Record):
    id: ID

class Event(faust.Record):
    event_type: str
    outcomes: List[Outcome]
    status: EventStatus 


class MarketBook(faust.Record):
    bids: Dict[Price, Volume]
    offers: Dict[Price, Volume]
