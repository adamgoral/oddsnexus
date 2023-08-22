from datetime import datetime
from dagster import AssetSelection, DailyPartitionsDefinition, ScheduleDefinition, asset, OpExecutionContext, Definitions, FilesystemIOManager, build_schedule_from_partitioned_job, define_asset_job

from oddsnexus.repositories.racing import SportingLifeSource

@asset(group_name='sporting_life', partitions_def=DailyPartitionsDefinition(start_date="2022-01-01"))
def sporting_life_horse_races(context: OpExecutionContext):
    source = SportingLifeSource('https://www.sportinglife.com/api')
    date_str = context.asset_partition_key_for_output()
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    races = source.list_races(date)
    context.add_output_metadata({
        'date': date,
        'races_count': len(races)
    })
    return races
