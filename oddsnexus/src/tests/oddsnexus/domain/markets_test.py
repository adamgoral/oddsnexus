import pytest

from oddsnexus.domain.markets import OrderBook


async def test_dump():
    expected = OrderBook(id='abc', event_id='123', bids=[], offers=[])
    actual = OrderBook.loads(expected.dumps())
    assert expected == actual