import datetime as dt
from typing import Dict, List

import faust

from oddsnexus.domain.common import Aggregate, ID

Price = int
Volume = int

class OrderBook(Aggregate):
    event_id: ID
    bids: Dict[Price, Volume]
    offers: Dict[Price, Volume]
