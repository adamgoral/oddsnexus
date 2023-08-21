
from datetime import date
import requests
from typing import Dict, List


class SportingLifeSource:
    
    def __init__(self, base_url: str) -> None:
        self._base_url = base_url
    
    def get_horses(self, horse_ids: List[str]) -> Dict[str, dict]:
        """
        Read horses details from SportingLife API.

        :param horse_ids: list of horse ids
        :return: dictionary of horse details for each id requested
        """
        result = {}
        for horse_id in horse_ids:
            request_url = f'{self._base_url}/horse-racing/horse/{horse_id}'
            response = requests.get(request_url)
            response.raise_for_status()
            result[horse_id] = response.json()
        return result
    
    def get_races(self, race_ids: List[str]) -> Dict[str, dict]:
        """
        Read races details from SportingLife API.
        
        :param race_ids: list of race ids
        :return: dictionary of race details for each id requested
        """
        result = {}
        for race_id in race_ids:
            request_url = f'{self._base_url}/horse-racing/race/{race_id}'
            response = requests.get(request_url)
            response.raise_for_status()
            result[race_id] = response.json()
        return result
    
    def list_races(self, as_of: date) -> List[dict]:
        """
        Get list of races for a given date.
        
        :param as_of: reference date
        :return: list of races details
        """
        request_url = f'{self._base_url}/horse-racing/racing/racecards/{as_of:%Y-%m-%d}'
        response = requests.get(request_url)
        response.raise_for_status()
        result = {}
        for item in response.json():
            race_ids = []
            for race in item['races']:
                race_id = race.get('race_summary_reference', {}).get('id', None)
                if race_id is None:
                    raise Exception(f'could not obtain race id from json data {race}')
                race_ids.append(race_id)
            races = self.get_races(race_ids)
            result.update(races)
        return list(result.values())
    