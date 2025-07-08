from dataclasses import dataclass
from datetime import datetime,timedelta
from typing import List
from models import DevOpsTask

@dataclass
class DevOpsMetrics:
    ticket_id: str
    developer: str
    team: str
    sprint: int

    first_commit_at: datetime
    deployed_at: datetime

    lead_time: timedelta
    cycle_time: timedelta
    coding_time: timedelta
    time_to_pr: timedelta
    pr_review_time: timedelta
    build_time: timedelta
    deploy_lag: timedelta
    total_work_time: timedelta


def compute_metrics_for_task(task: DevOpsTask) -> DevOpsMetrics:
    return DevOpsMetrics(
        ticket_id=task.ticket_id,
        developer=task.developer,
        team=task.team,
        sprint=task.sprint,

        first_commit_at=task.first_commit_at,
        deployed_at=task.deployed_at,

        lead_time=task.deployed_at - task.created_at,
        cycle_time=task.deployed_at - task.in_progress_at,
        coding_time=task.first_commit_at - task.in_progress_at,
        time_to_pr=task.pr_created_at - task.first_commit_at,
        pr_review_time=task.pr_merged_at - task.pr_created_at,
        build_time=task.deployed_at - task.build_started_at,
        deploy_lag=task.deployed_at - task.pr_merged_at,
        total_work_time=task.deployed_at - task.first_commit_at,
    )

def compute_all_metrics(tasks: List[DevOpsTask]) -> List[DevOpsMetrics]:
    return [compute_metrics_for_task(task) for task in tasks]


# ----------------------------
# DORA Metrics Calculation
# ----------------------------
def compute_dora_metrics(tasks: List[DevOpsTask]) -> dict:
    if not tasks:
        return {}

    # Deployment Frequency
    deploy_dates = [task.deployed_at.date() for task in tasks]
    unique_days = len(set(deploy_dates))
    deployments_per_day = len(deploy_dates) / unique_days if unique_days else 0

    # Lead Time for Changes
    lead_times = [(task.deployed_at - task.first_commit_at).total_seconds() / 3600 for task in tasks]
    avg_lead_time_hrs = sum(lead_times) / len(lead_times)

    # Change Failure Rate
    failed_deploys = [task for task in tasks if not getattr(task, 'deployment_success', True)]
    change_failure_rate = len(failed_deploys) / len(tasks) if tasks else 0

    # Mean Time to Restore
    restore_durations = [
        (task.restore_time - task.deployed_at).total_seconds() / 3600
        for task in failed_deploys if getattr(task, 'restore_time', None)
    ]
    mttr = sum(restore_durations) / len(restore_durations) if restore_durations else 0

    return {
        "deployment_frequency_per_day": round(deployments_per_day, 2),
        "average_lead_time_hours": round(avg_lead_time_hrs, 2),
        "change_failure_rate_percent": round(change_failure_rate * 100, 2),
        "mean_time_to_restore_hours": round(mttr, 2)
    }


if __name__ == "__main__":
    from generate_data import generate_synthetic_tasks

    tasks = generate_synthetic_tasks(50)

    print("📊 Individual Workflow Metrics:")
    metrics = compute_all_metrics(tasks)
    for m in metrics[:3]:
        print(m)

    print("\n📈 DORA Metrics:")
    dora = compute_dora_metrics(tasks)
    for k, v in dora.items():
        print(f"{k}: {v}")
