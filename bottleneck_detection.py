from compute_metrics import DevOpsMetrics
from statistics import mean, stdev
from typing import List, Dict
from datetime import timedelta

# Define a function to detect task-level bottlenecks
def detect_bottlenecks(metrics_list: List[DevOpsMetrics]) -> List[Dict]:
    # Compute mean and stdev per metric across tasks
    metric_fields = [
        'lead_time',
        'cycle_time',
        'coding_time',
        'time_to_pr',
        'pr_review_time',
        'build_time',
        'deploy_lag',
        'total_work_time',
    ]

    # Convert durations to seconds
    def duration_in_seconds(metric: timedelta) -> float:
        return metric.total_seconds()

    # Prepare per-field stats
    field_stats = {}
    for field in metric_fields:
        values = [duration_in_seconds(getattr(m, field)) for m in metrics_list]
        field_stats[field] = {
            'mean': mean(values),
            'stdev': stdev(values) if len(values) > 1 else 0.0,
            'threshold': mean(values) + 1.0 * stdev(values)  # simple outlier rule
        }

    # Detect per-task bottlenecks
    bottlenecks = []
    for m in metrics_list:
        task_bottlenecks = []

        for field in metric_fields:
            value_sec = duration_in_seconds(getattr(m, field))
            if value_sec > field_stats[field]['threshold']:
                task_bottlenecks.append(field)

        bottlenecks.append({
            'ticket_id': m.ticket_id,
            'developer': m.developer,
            'team': m.team,
            'bottlenecks': task_bottlenecks
        })

    return bottlenecks

from collections import defaultdict

def aggregate_bottlenecks(bottleneck_reports: List[Dict]) -> Dict:
    team_stats = defaultdict(int)
    dev_stats = defaultdict(int)
    stage_stats = defaultdict(int)

    for report in bottleneck_reports:
        for stage in report['bottlenecks']:
            team_stats[report['team']] += 1
            dev_stats[report['developer']] += 1
            stage_stats[stage] += 1

    return {
        'by_team': dict(team_stats),
        'by_developer': dict(dev_stats),
        'by_stage': dict(stage_stats)
    }
