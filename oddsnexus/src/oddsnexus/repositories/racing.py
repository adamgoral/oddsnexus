
from datetime import date
import requests
from typing import List

from oddsnexus.domain.sports import HorseRace


class SportingLifeSource:
    
    def __init__(self, base_url: str) -> None:
        self._base_url = base_url
    
    def get_horses(self, horse_ids: List[str]) -> List[dict]:
        pass
    
    def get_races(self, race_ids: List[str]) -> List[HorseRace]:
        result = []
        for race_id in race_ids:
            request_url = f'{self._base_url}/horse-racing/race/{race_id}'
            response = requests.get(request_url)
            response.raise_for_status()
            result.append(HorseRace.from_dict(response.json()))
        return result
    
    def list_races(self, as_of: date) -> List[dict]:
        request_url = f'{self._base_url}/horse-racing/racing/racecards/{as_of:%Y-%m-%d}'
        response = requests.get(request_url)
        response.raise_for_status()
        result = []
        for item in response.json():
            race_ids = []
            for race in item['races']:
                race_id = race.get('race_summary_reference', {}).get('id', None)
                race_ids.append(race_id)
            races = self.get_races(race_ids)
            result += races
        return result
    