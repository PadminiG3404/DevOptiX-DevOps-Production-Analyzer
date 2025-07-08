import matplotlib.pyplot as plt
import seaborn as sns
from compute_metrics import DevOpsMetrics
from typing import List, Optional
from collections import Counter
from compute_metrics import compute_dora_metrics
from generate_data import generate_synthetic_tasks

sns.set(style="whitegrid")


def plot_stage_distribution(
    metrics: List[DevOpsMetrics], 
    field: str, 
    save_path: Optional[str] = None
):
    """Plot histogram for a given stage duration across DevOps tasks."""
    try:
        durations = [getattr(m, field).total_seconds() / 3600 for m in metrics]
    except AttributeError:
        print(f"[ERROR] Field '{field}' not found in DevOpsMetrics.")
        return

    plt.figure(figsize=(10, 6))
    sns.histplot(durations, kde=True, color="skyblue")
    plt.title(f"Distribution of {field.replace('_', ' ').title()} (Hours)")
    plt.xlabel("Hours")
    plt.ylabel("Number of Tasks")

    if save_path:
        plt.savefig(save_path)
        print(f"[VISUAL] Saved plot to {save_path}")
    else:
        plt.show()
    plt.close()


def plot_bottleneck_counts(
    bottlenecks: List[dict], 
    save_path: Optional[str] = None
):
    """Plot count of bottlenecks by stage across all tasks."""
    all_stages = [stage for b in bottlenecks for stage in b.get("bottlenecks", [])]
    counts = Counter(all_stages)

    if not counts:
        print("[INFO] No bottlenecks to plot.")
        return

    plt.figure(figsize=(10, 6))
    sns.barplot(x=list(counts.keys()), y=list(counts.values()), hue=list(counts.keys()), dodge=False, palette="Reds", legend=False)
    plt.title("Bottlenecks by Stage")
    plt.xlabel("Stage")
    plt.ylabel("Count")
    plt.xticks(rotation=30)

    if save_path:
        plt.savefig(save_path)
        print(f"[VISUAL] Saved bottleneck plot to {save_path}")
    else:
        plt.show()
    plt.close()

def plot_dora_metrics(dora: dict, save_path: Optional[str] = None):
    """Visualize DORA metrics in a bar chart."""
    if not dora:
        print("[INFO] No DORA metrics available to plot.")
        return

    keys = list(dora.keys())
    values = list(dora.values())

    plt.figure(figsize=(8, 5))
    sns.barplot(x=keys, y=values, palette="Blues_d")
    plt.title("DORA Metrics Overview")
    plt.ylabel("Value")
    plt.xticks(rotation=30)

    if save_path:
        plt.savefig(save_path)
        print(f"[VISUAL] Saved DORA metrics plot to {save_path}")
    else:
        plt.show()
    plt.close()



# Optional usage example (not required in production):
if __name__ == "__main__":
    from generate_data import generate_synthetic_tasks
    from compute_metrics import compute_all_metrics
    from bottleneck_detection import detect_bottlenecks

    tasks = generate_synthetic_tasks(50)
    metrics = compute_all_metrics(tasks)
    bottlenecks = detect_bottlenecks(metrics)
    dora = compute_dora_metrics(tasks)

    plot_stage_distribution(metrics, "pr_review_time")
    plot_bottleneck_counts(bottlenecks)
    plot_dora_metrics(dora)
