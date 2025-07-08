from collections import defaultdict
from statistics import mean
from typing import List
from compute_metrics import DevOpsMetrics

def analyze_trends(metrics: List[DevOpsMetrics]):
    """
    Analyze per-developer metric trends over sprints.
    Flags regressions where the latest sprint worsens by >20% vs. previous average.
    """
    trends_by_dev = defaultdict(lambda: defaultdict(list))

    for m in metrics:
        if not hasattr(m, "sprint"):
            continue  # Skip if sprint info is missing
        trends_by_dev[m.developer]["pr_review_time"].append((m.sprint, m.pr_review_time.total_seconds()))
        trends_by_dev[m.developer]["cycle_time"].append((m.sprint, m.cycle_time.total_seconds()))
        trends_by_dev[m.developer]["lead_time"].append((m.sprint, m.lead_time.total_seconds()))

    regression_warnings = []

    for dev, metric_data in trends_by_dev.items():
        for metric_name, values in metric_data.items():
            values.sort()
            sprints, durations = zip(*values)

            if len(durations) >= 3:
                past_avg = mean(durations[:-1])
                if past_avg == 0:
                    continue
                if durations[-1] > 1.2 * past_avg:
                    regression_warnings.append({
                        "developer": dev,
                        "metric": metric_name,
                        "sprint": sprints[-1],
                        "previous_avg": round(past_avg, 2),
                        "current": round(durations[-1], 2),
                        "message": f"{metric_name} increased by over 20% in sprint {sprints[-1]}"
                    })

    return regression_warnings
