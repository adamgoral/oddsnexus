import pytest

from oddsnexus.domain.markets import OrderBook


async def test_dump():
    OrderBook(event_id='', bids=[], offers=[]).dumps()