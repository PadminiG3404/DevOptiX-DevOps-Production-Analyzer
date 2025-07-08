import os
from generate_data import generate_synthetic_tasks
from compute_metrics import compute_all_metrics, compute_dora_metrics
from bottleneck_detection import detect_bottlenecks
from recommendation_engine import generate_all_recommendations, generate_dora_insights
from export import export_metrics_to_csv, export_json
from trend_analysis import analyze_trends
from ml_anomaly_detector import detect_anomalies
from visualize import (
    plot_stage_distribution,
    plot_bottleneck_counts,
    plot_dora_metrics,
    plot_bottlenecks_by_stage_and_team,
    plot_avg_stage_durations,
    plot_dora_trends_over_sprints,
    plot_developer_stage_heatmap
)
# Main script to run the DevOps production analysis pipeline

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run():
    print("🔧 Generating synthetic data...")
    tasks = generate_synthetic_tasks(100)

    print("📊 Computing metrics...")
    metrics = compute_all_metrics(tasks)

    print("🔍 Detecting bottlenecks...")
    bottlenecks = detect_bottlenecks(metrics)

    print("💡 Generating task-based recommendations...")
    task_ids_with_bottlenecks = {b["ticket_id"] for b in bottlenecks}
    filtered_metrics = [m for m in metrics if m.ticket_id in task_ids_with_bottlenecks]
    task_recs = generate_all_recommendations(filtered_metrics)


    print("📈 Computing DORA metrics...")
    dora_metrics = compute_dora_metrics(tasks)

    print("💡 Generating DORA-based recommendations...")
    dora_recs = generate_dora_insights(tasks)

    print("📉 Running trend analysis...")
    trends = analyze_trends(metrics)

    print("🤖 Running anomaly detection...")
    anomalies = detect_anomalies(metrics)

    print("📤 Exporting outputs...")
    export_metrics_to_csv(metrics, os.path.join(OUTPUT_DIR, "metrics.csv"))
    export_json(bottlenecks, os.path.join(OUTPUT_DIR, "bottlenecks.json"))
    export_json(task_recs, os.path.join(OUTPUT_DIR, "task_recommendations.json"))
    export_json(dora_recs, os.path.join(OUTPUT_DIR, "dora_recommendations.json"))
    export_json(trends, os.path.join(OUTPUT_DIR, "trend_regressions.json"))
    export_json(anomalies, os.path.join(OUTPUT_DIR, "anomalies.json"))

    # Export recommendations as readable text
    with open(os.path.join(OUTPUT_DIR, "task_recommendations.txt"), "w") as f:
        for rec in task_recs:
            f.write(f"{rec}\n")

    with open(os.path.join(OUTPUT_DIR, "dora_recommendations.txt"), "w") as f:
        for rec in dora_recs:
            f.write(f"{rec}\n")

    # Export DORA metrics
    with open(os.path.join(OUTPUT_DIR, "dora_metrics.txt"), "w") as f:
        for k, v in dora_metrics.items():
            f.write(f"{k}: {v}\n")

    print("📊 Plotting insights...")
    plot_stage_distribution(metrics, "pr_review_time")
    plot_bottleneck_counts(bottlenecks)
    plot_dora_metrics(dora_metrics)
    plot_bottlenecks_by_stage_and_team(bottlenecks)
    plot_avg_stage_durations(metrics)   
    plot_dora_trends_over_sprints(metrics)
    plot_developer_stage_heatmap(bottlenecks)

    plot_stage_distribution(
        metrics, os.path.join(OUTPUT_DIR, "pr_review_time_distribution.png")
    )
    plot_bottleneck_counts(
        bottlenecks, os.path.join(OUTPUT_DIR, "bottleneck_counts.png")
    )
    plot_dora_metrics(
        dora_metrics, os.path.join(OUTPUT_DIR, "dora_metrics.png")
    )
    plot_bottlenecks_by_stage_and_team(
        bottlenecks, os.path.join(OUTPUT_DIR, "bottlenecks_by_stage_and_team.png")
    )
    plot_avg_stage_durations(
        metrics, os.path.join(OUTPUT_DIR, "avg_pr_review_time_by_team.png")
    )
    plot_dora_trends_over_sprints(
        metrics, os.path.join(OUTPUT_DIR, "lead_time_trend.png")
    )
    plot_developer_stage_heatmap(
        bottlenecks, os.path.join(OUTPUT_DIR, "developer_stage_heatmap.png")
    )

    print("✅ Done. Check the 'outputs/' folder for results.")
    print("\n📈 DORA Metrics Summary:")
    for k, v in dora_metrics.items():
        print(f"   {k}: {v}")

if __name__ == "__main__":
    run()
