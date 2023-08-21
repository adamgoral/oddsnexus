from datetime import datetime
from dagster import AssetSelection, DailyPartitionsDefinition, ScheduleDefinition, asset, OpExecutionContext, Definitions, FilesystemIOManager, build_schedule_from_partitioned_job, define_asset_job

from oddsnexus.repositories.racing import SportingLifeSource

@asset(partitions_def=DailyPartitionsDefinition(start_date="2022-01-01"))
def sporting_life_horse_races(context: OpExecutionContext):
    source = SportingLifeSource('https://www.sportinglife.com/api')
    date_str = context.asset_partition_key_for_output()
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    races = source.list_races(date)
    context.add_output_metadata({
        'races_count': len(races)
    })
    return races


partitioned_asset_job = define_asset_job("partitioned_job", selection=[sporting_life_horse_races], partitions_def=DailyPartitionsDefinition(start_date="2022-01-01"))


asset_partitioned_schedule = build_schedule_from_partitioned_job(
    partitioned_asset_job
)


defs = Definitions(
    assets=[sporting_life_horse_races],
    resources={
        'io_manager': FilesystemIOManager(base_dir='./data')
    },
    schedules=[asset_partitioned_schedule],
    jobs=[partitioned_asset_job]
)
