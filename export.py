import csv
import json
from typing import List, Dict
from compute_metrics import DevOpsMetrics

def export_metrics_to_csv(metrics: List[DevOpsMetrics], filename: str = "metrics.csv") -> None:
    if not metrics:
        print(f"[WARN] No metrics to export to {filename}")
        return

    with open(filename, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(metrics[0].__dataclass_fields__.keys())
        for m in metrics:
            writer.writerow([getattr(m, field) for field in metrics[0].__dataclass_fields__])

    print(f"[EXPORT] Metrics exported to {filename}")


def export_json(data: List[dict], filename: str) -> None:
    if not data:
        print(f"[WARN] No data to export to {filename}")
        return

    with open(filename, "w") as f:
        json.dump(data, f, indent=2, default=str)

    print(f"[EXPORT] JSON data exported to {filename}")


def export_dora_metrics(dora_metrics: Dict[str, float], filename: str = "dora_metrics.json") -> None:
    with open(filename, "w") as f:
        json.dump(dora_metrics, f, indent=2)

    print(f"[EXPORT] DORA metrics exported to {filename}")


# Optional test runner
if __name__ == "__main__":
    from generate_data import generate_synthetic_tasks
    from compute_metrics import compute_all_metrics, compute_dora_metrics
    from bottleneck_detection import detect_bottlenecks
    from recommendations import generate_recommendations

    tasks = generate_synthetic_tasks(50)
    metrics = compute_all_metrics(tasks)
    bottlenecks = detect_bottlenecks(metrics)
    recommendations = generate_recommendations(bottlenecks)
    dora = compute_dora_metrics(tasks)

    export_metrics_to_csv(metrics, "devops_metrics.csv")
    export_json(bottlenecks, "bottlenecks.json")
    export_json(recommendations, "recommendations.json")
    export_dora_metrics(dora, "dora_metrics.json")
