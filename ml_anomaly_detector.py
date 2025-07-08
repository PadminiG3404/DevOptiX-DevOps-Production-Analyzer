from sklearn.ensemble import IsolationForest
from compute_metrics import DevOpsMetrics
from typing import List, Dict

def detect_anomalies(metrics: List[DevOpsMetrics]) -> List[Dict]:
    """
    Use Isolation Forest to detect anomalous task metrics.
    Flags tasks with behavior deviating significantly from the norm.
    """
    data = []
    meta = []

    for m in metrics:
        try:
            data.append([
                m.pr_review_time.total_seconds(),
                m.cycle_time.total_seconds(),
                m.lead_time.total_seconds(),
                m.build_time.total_seconds(),
            ])
            meta.append({
                "ticket_id": m.ticket_id,
                "developer": m.developer,
                "team": m.team,
                "pr_review_time": round(m.pr_review_time.total_seconds(), 2),
                "cycle_time": round(m.cycle_time.total_seconds(), 2),
                "lead_time": round(m.lead_time.total_seconds(), 2),
                "build_time": round(m.build_time.total_seconds(), 2)
            })
        except AttributeError:
            continue  # Skip metrics missing expected fields

    if not data:
        return []

    model = IsolationForest(contamination=0.1, random_state=42)
    predictions = model.fit_predict(data)

    anomalies = []
    for i, label in enumerate(predictions):
        if label == -1:
            anomalies.append({
                **meta[i],
                "issue": "Anomalous task behavior detected"
            })

    return anomalies
