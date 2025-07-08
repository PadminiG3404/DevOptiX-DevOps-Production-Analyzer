from typing import List, Dict
from compute_metrics import DevOpsMetrics, compute_dora_metrics
from models import DevOpsTask

# Thresholds (tunable or make config-driven)
DORA_THRESHOLDS = {
    "deployment_frequency_per_day": 1.0,          # < 1 deploy/day = low
    "average_lead_time_hours": 48.0,              # > 48 hrs = high
    "mean_time_to_restore_hours": 4.0,            # > 4 hrs
    "change_failure_rate_percent": 20.0           # > 20%
}


def generate_task_recommendations(m: DevOpsMetrics) -> List[Dict]:
    recs = []

    if m.pr_review_time.total_seconds() > 36 * 3600:
        recs.append({
            "category": "Code Review",
            "severity": "High",
            "message": "PR reviews are slow. Encourage smaller PRs, rotate reviewers, or enforce SLAs."
        })

    if m.lead_time.total_seconds() > 5 * 86400:
        recs.append({
            "category": "Process",
            "severity": "High",
            "message": "Lead time is too high. Reassess delays across planning to delivery."
        })

    if m.deploy_lag.total_seconds() > 2 * 3600:
        recs.append({
            "category": "Deployment",
            "severity": "Medium",
            "message": "Deployments are delayed post-merge. Consider continuous delivery triggers."
        })

    if m.build_time.total_seconds() > 1800:
        recs.append({
            "category": "CI/CD",
            "severity": "Medium",
            "message": "Builds are slow. Optimize pipelines, cache dependencies, or parallelize tests."
        })

    if m.cycle_time.total_seconds() > 4 * 86400:
        recs.append({
            "category": "Development",
            "severity": "High",
            "message": "Cycle time is high. Investigate blockers during development or QA delays."
        })

    return recs


def generate_all_recommendations(metrics_list: List[DevOpsMetrics]) -> List[Dict]:
    all_recs = []

    for m in metrics_list:
        task_recs = generate_task_recommendations(m)
        if task_recs:
            all_recs.append({
                "ticket_id": m.ticket_id,
                "developer": m.developer,
                "team": m.team,
                "recommendations": task_recs
            })

    return all_recs


def generate_dora_recommendations(dora: Dict) -> List[Dict]:
    recs = []

    if dora["deployment_frequency_per_day"] < DORA_THRESHOLDS["deployment_frequency_per_day"]:
        recs.append({
            "category": "Deployment Frequency",
            "severity": "High",
            "message": "Low deployment frequency. Automate release processes and reduce batch size."
        })

    if dora["average_lead_time_hours"] > DORA_THRESHOLDS["average_lead_time_hours"]:
        recs.append({
            "category": "Lead Time",
            "severity": "High",
            "message": "High lead time for changes. Optimize development workflows and CI/CD stages."
        })

    if dora["mean_time_to_restore_hours"] > DORA_THRESHOLDS["mean_time_to_restore_hours"]:
        recs.append({
            "category": "Reliability",
            "severity": "High",
            "message": "MTTR is high. Invest in monitoring, alerting, and rollback strategies."
        })

    if dora["change_failure_rate_percent"] > DORA_THRESHOLDS["change_failure_rate_percent"]:
        recs.append({
            "category": "Change Quality",
            "severity": "High",
            "message": "Change failure rate is high. Strengthen testing, peer reviews, and CI coverage."
        })

    return recs

def generate_dora_insights(tasks: List[DevOpsTask]) -> List[Dict]:
    dora = compute_dora_metrics(tasks)
    return generate_dora_recommendations(dora)
