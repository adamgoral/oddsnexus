from datetime import date
import pytest

from oddsnexus.repositories.racing import SportingLifeSource


def test_list_races():
    repository = SportingLifeSource('https://www.sportinglife.com/api')
    as_of = date(2021, 1, 1)
    actual = repository.list_races(as_of)
    pass
