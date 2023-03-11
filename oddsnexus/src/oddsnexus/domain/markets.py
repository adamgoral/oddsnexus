import datetime as dt
from typing import Dict, List

from oddsnexus.domain.common import Aggregate, UniqueId

Price = int
Volume = int

class OrderBook(Aggregate):
    event_id: UniqueId
    bids: Dict[Price, Volume]
    offers: Dict[Price, Volume]
