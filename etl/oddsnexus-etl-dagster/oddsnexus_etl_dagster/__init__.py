from dagster import DailyPartitionsDefinition, Definitions, FilesystemIOManager, build_schedule_from_partitioned_job, define_asset_job, load_assets_from_modules

from . import assets

all_assets = load_assets_from_modules([assets])


partitioned_asset_job = define_asset_job("partitioned_job",
                                         selection=all_assets,
                                         partitions_def=DailyPartitionsDefinition(start_date="2022-01-01"))


asset_partitioned_schedule = build_schedule_from_partitioned_job(
    partitioned_asset_job,
    hour_of_day=2
)


defs = Definitions(
    assets=all_assets,
    resources={
        'io_manager': FilesystemIOManager(base_dir='./data')
    },
    schedules=[asset_partitioned_schedule],
    jobs=[partitioned_asset_job]
)