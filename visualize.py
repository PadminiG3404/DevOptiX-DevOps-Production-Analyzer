import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from collections import Counter, defaultdict
from typing import List, Optional
from compute_metrics import DevOpsMetrics

sns.set(style="whitegrid")


def plot_stage_distribution(metrics: List[DevOpsMetrics], field: str, save_path: Optional[str] = None):
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


def plot_bottleneck_counts(bottlenecks: List[dict], save_path: Optional[str] = None):
    all_stages = [stage for b in bottlenecks for stage in b.get("bottlenecks", [])]
    counts = Counter(all_stages)

    if not counts:
        print("[INFO] No bottlenecks to plot.")
        return

    plt.figure(figsize=(10, 6))
    sns.barplot(x=list(counts.keys()), y=list(counts.values()), hue=list(counts.keys()), palette="Reds", legend=False)
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
    if not dora:
        print("[INFO] No DORA metrics available to plot.")
        return

    keys = list(dora.keys())
    values = list(dora.values())

    plt.figure(figsize=(8, 5))
    sns.barplot(x=keys, y=values, palette="Blues_d", hue=keys, legend=False)

    plt.title("DORA Metrics Overview")
    plt.ylabel("Value")
    plt.xticks(rotation=30)

    if save_path:
        plt.savefig(save_path)
        print(f"[VISUAL] Saved DORA metrics plot to {save_path}")
    else:
        plt.show()
    plt.close()


def plot_bottlenecks_by_stage_and_team(bottlenecks: List[dict], save_path: Optional[str] = None):
    records = []
    for b in bottlenecks:
        team = b.get("team")
        for stage in b.get("bottlenecks", []):
            records.append({"stage": stage, "team": team})
    if not records:
        print("[INFO] No data to plot for bottlenecks by stage and team.")
        return

    df = pd.DataFrame(records)
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x="stage", hue="team", palette="Set2")
    plt.title("Bottlenecks by Stage and Team")
    plt.xlabel("Pipeline Stage")
    plt.ylabel("Count")
    plt.xticks(rotation=30)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        print(f"[VISUAL] Saved plot to {save_path}")
    else:
        plt.show()
    plt.close()


def plot_avg_stage_durations(metrics: List[DevOpsMetrics], save_path: Optional[str] = None):
    df = pd.DataFrame([m.__dict__ for m in metrics])
    df['pr_review_time_hrs'] = df['pr_review_time'].dt.total_seconds() / 3600
    avg = df.groupby("team")['pr_review_time_hrs'].mean().sort_values()

    plt.figure(figsize=(10, 6))
    avg.plot(kind='barh', color='coral')
    plt.title("Average PR Review Time by Team")
    plt.xlabel("Hours")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        print(f"[VISUAL] Saved avg stage durations to {save_path}")
    else:
        plt.show()
    plt.close()


def plot_dora_trends_over_sprints(metrics: List[DevOpsMetrics], save_path: Optional[str] = None):
    df = pd.DataFrame([m.__dict__ for m in metrics])
    df['lead_time_hours'] = (df['deployed_at'] - df['first_commit_at']).dt.total_seconds() / 3600

    if 'sprint' not in df.columns:
        print("[WARN] Sprint field missing. Cannot plot DORA trends.")
        return

    sprint_means = df.groupby("sprint")["lead_time_hours"].mean()

    plt.figure(figsize=(10, 5))
    sprint_means.plot(marker='o', linestyle='-', color='blue')
    plt.title("Lead Time per Sprint")
    plt.xlabel("Sprint")
    plt.ylabel("Avg Lead Time (Hours)")
    plt.grid(True)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        print(f"[VISUAL] Saved DORA trends to {save_path}")
    else:
        plt.show()
    plt.close()


def plot_developer_stage_heatmap(bottlenecks: List[dict], save_path: Optional[str] = None):
    records = []
    for b in bottlenecks:
        dev = b.get("developer")
        for stage in b.get("bottlenecks", []):
            records.append({"developer": dev, "stage": stage})
    if not records:
        print("[INFO] No developer bottlenecks to plot.")
        return

    df = pd.DataFrame(records)
    heatmap_data = df.groupby(['developer', 'stage']).size().unstack(fill_value=0)

    plt.figure(figsize=(10, 6))
    sns.heatmap(heatmap_data, annot=True, fmt='d', cmap="YlGnBu")
    plt.title("Bottlenecks per Developer by Stage")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        print(f"[VISUAL] Saved heatmap to {save_path}")
    else:
        plt.show()
    plt.close()


