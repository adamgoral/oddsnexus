from datetime import date, datetime, timedelta
from dagster import Definitions, FilesystemIOManager, build_schedule_from_partitioned_job, define_asset_job, schedule, RunRequest, ScheduleEvaluationContext

from oddsnexus_etl_dagster.assets import sporting_life_horse_race_results, sporting_life_upcoming_horse_races, daily_partition

all_assets = [sporting_life_horse_race_results, sporting_life_upcoming_horse_races]


results_job = define_asset_job("results_job", selection=[sporting_life_horse_race_results])

upcoming_events_job = define_asset_job('upcoming_events_job', selection=[sporting_life_upcoming_horse_races], partitions_def=daily_partition)

results_schedule = build_schedule_from_partitioned_job(
    results_job,
    hour_of_day=2
)


@schedule(cron_schedule='0 2 * * *', job=upcoming_events_job)
def future_schedule(context: ScheduleEvaluationContext):
    as_of = context.scheduled_execution_time
    for x in range(10):
        key = as_of + timedelta(days=x)
        key_str = key.strftime('%Y-%m-%d')
        yield RunRequest(run_key=key_str, partition_key=key_str)
    

defs = Definitions(
    assets=all_assets,
    resources={
        'io_manager': FilesystemIOManager(base_dir='./data')
    },
    schedules=[results_schedule, future_schedule],
    jobs=[results_job, upcoming_events_job]
)
