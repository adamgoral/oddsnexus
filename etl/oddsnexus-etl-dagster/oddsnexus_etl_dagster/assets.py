from datetime import date, datetime
from typing import List
from dagster import DailyPartitionsDefinition, asset, AssetExecutionContext, op, OpExecutionContext

from oddsnexus.repositories.racing import SportingLifeSource

daily_partition = DailyPartitionsDefinition(start_date="2022-01-01", end_offset=10)

@op
def read_sporting_life_horse_races(as_of: date) -> List[dict]:
    print(f'read_sporting_life_horse_races {as_of} {type(as_of)}')
    source = SportingLifeSource('https://www.sportinglife.com/api')
    races = source.list_races(as_of)
    return races


@asset(group_name='sporting_life', partitions_def=daily_partition)
def sporting_life_horse_race_results(context: AssetExecutionContext) -> List[dict]:
    date_str = context.asset_partition_key_for_output()
    as_of = datetime.strptime(date_str, "%Y-%m-%d").date()
    races = read_sporting_life_horse_races(as_of=as_of)
    context.add_output_metadata({
        'date': date_str,
        'races_count': len(races)
    })
    return races


@asset(group_name='sporting_life', partitions_def=daily_partition)
def sporting_life_upcoming_horse_races(context: AssetExecutionContext) -> List[dict]:
    date_str = context.asset_partition_key_for_output()
    as_of = datetime.strptime(date_str, "%Y-%m-%d").date()
    print(f'sporting_life_upcoming_horse_races {as_of} {type(as_of)}')
    races = read_sporting_life_horse_races(as_of=as_of)
    context.add_output_metadata({
        'date': date_str,
        'races_count': len(races)
    })
    return races
