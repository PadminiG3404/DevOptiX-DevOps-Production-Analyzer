from compute_metrics import DevOpsMetrics
from statistics import mean
from typing import List, Dict
from datetime import timedelta
from collections import defaultdict
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import numpy as np

# Heuristic and ML-based bottleneck detection
def detect_bottlenecks(metrics_list: List[DevOpsMetrics]) -> List[Dict]:
    metric_fields = [
        'lead_time', 'cycle_time', 'coding_time', 'time_to_pr',
        'pr_review_time', 'build_time', 'deploy_lag', 'total_work_time',
    ]
    
    def duration_in_seconds(metric: timedelta) -> float:
        return metric.total_seconds()

    # Step 1: Heuristic bottlenecks based on 80th percentile
    field_thresholds = {}
    for field in metric_fields:
        values = [duration_in_seconds(getattr(m, field)) for m in metrics_list]
        field_thresholds[field] = np.percentile(values, 80)

    bottlenecks = []
    duration_matrix = []

    for m in metrics_list:
        task_bottlenecks = []
        vector = []

        for field in metric_fields:
            value = duration_in_seconds(getattr(m, field))
            vector.append(value)
            if value > field_thresholds[field]:
                task_bottlenecks.append(field)

        bottlenecks.append({
            'ticket_id': m.ticket_id,
            'developer': m.developer,
            'team': m.team,
            'bottlenecks': task_bottlenecks,
            'heuristic': bool(task_bottlenecks),
            'ml_flag': False
        })
        duration_matrix.append(vector)

    # Step 2: ML-based bottlenecks using IsolationForest
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(duration_matrix)
    model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
    preds = model.fit_predict(X_scaled)

    for idx, pred in enumerate(preds):
        if pred == -1:
            bottlenecks[idx]['ml_flag'] = True
            if not bottlenecks[idx]['bottlenecks']:
                bottlenecks[idx]['bottlenecks'].append('ml_detected')

    return bottlenecks

# Aggregation utility for bottleneck insights
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
