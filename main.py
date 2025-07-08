import os
from generate_data import generate_synthetic_tasks
from compute_metrics import compute_all_metrics, compute_dora_metrics
from bottleneck_detection import detect_bottlenecks
from recommendation_engine import generate_all_recommendations
from visualize import plot_stage_distribution, plot_bottleneck_counts, plot_dora_metrics
from export import export_metrics_to_csv, export_json

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run():
    print("🔧 Generating synthetic data...")
    tasks = generate_synthetic_tasks(100)

    print("📊 Computing metrics...")
    metrics = compute_all_metrics(tasks)

    print("🔍 Detecting bottlenecks...")
    bottlenecks = detect_bottlenecks(metrics)

    print("💡 Generating recommendations...")
    recommendations = generate_all_recommendations(bottlenecks)

    print("📤 Exporting outputs...")
    export_metrics_to_csv(metrics, os.path.join(OUTPUT_DIR, "metrics.csv"))
    export_json(bottlenecks, os.path.join(OUTPUT_DIR, "bottlenecks.json"))

    # Export recommendations
    with open(os.path.join(OUTPUT_DIR, "recommendations.txt"), "w") as f:
        for rec in recommendations:
            f.write(f"{rec}\n")

    # DORA metrics
    dora = compute_dora_metrics(tasks)
    with open(os.path.join(OUTPUT_DIR, "dora_metrics.txt"), "w") as f:
        for k, v in dora.items():
            f.write(f"{k}: {v}\n")

    print("📈 Plotting insights...")
    plot_stage_distribution(metrics, "pr_review_time")
    plot_bottleneck_counts(bottlenecks)
    plot_dora_metrics(dora)

    print("✅ Done. Check the 'outputs/' folder for results.")
    print("\n📈 DORA Metrics Summary:")
    for k, v in dora.items():
        print(f"   {k}: {v}")

if __name__ == "__main__":
    run()
