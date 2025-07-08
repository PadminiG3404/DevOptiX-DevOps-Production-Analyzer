from typing import List, Dict

# Static mapping of bottleneck types to recommendations
RECOMMENDATION_MAP = {
    'lead_time': [
        "Re-evaluate ticket prioritization or backlog grooming processes.",
        "Reduce handoffs between planning and development."
    ],
    'cycle_time': [
        "Identify blockers during development.",
        "Use task breakdown for large stories to improve visibility."
    ],
    'coding_time': [
        "Consider pairing or early feedback on complex tasks.",
        "Check if requirements were unclear or too broad."
    ],
    'time_to_pr': [
        "Encourage smaller, more frequent commits.",
        "Promote earlier PR creation for parallel review."
    ],
    'pr_review_time': [
        "Add more reviewers or automate basic code checks.",
        "Set SLAs for PR response times within the team."
    ],
    'build_time': [
        "Optimize build pipeline or use parallel jobs.",
        "Check for flaky or slow integration tests."
    ],
    'deploy_lag': [
        "Automate deployment triggers post-merge.",
        "Evaluate why merged code is waiting (e.g., batch deploys?)."
    ],
    'total_work_time': [
        "Look into cross-team coordination or context switching delays.",
        "Encourage working in focused sprints with WIP limits."
    ]
}

def generate_recommendations(bottleneck_report: Dict) -> Dict:
    """
    Input: Single bottleneck report for a task
    Output: Dict with recommendations
    """
    suggestions = []
    for stage in bottleneck_report['bottlenecks']:
        stage_recs = RECOMMENDATION_MAP.get(stage, [])
        suggestions.extend(stage_recs)

    return {
        'ticket_id': bottleneck_report['ticket_id'],
        'developer': bottleneck_report['developer'],
        'team': bottleneck_report['team'],
        'bottlenecks': bottleneck_report['bottlenecks'],
        'recommendations': suggestions
    }

def generate_all_recommendations(bottleneck_reports: List[Dict]) -> List[Dict]:
    return [generate_recommendations(report) for report in bottleneck_reports]
