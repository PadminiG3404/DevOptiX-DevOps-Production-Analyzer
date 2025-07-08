import random
from datetime import datetime, timedelta
from typing import List
from models import DevOpsTask  
import csv

def generate_synthetic_tasks(num_tasks: int = 100) -> List[DevOpsTask]:
    devs = ['alice', 'bob', 'carol', 'dave']
    teams = ['backend', 'frontend', 'platform', 'qa']
    base_time = datetime(2025, 7, 1, 9, 0, 0)

    tasks = []

    for i in range(num_tasks):
        ticket_id = f"TASK-{i + 1}"
        developer = random.choice(devs)
        team = random.choice(teams)
        sprint = i // 10  # Every 10 tasks belong to one sprint

        # Start time for task (spread over 10 working days)
        created_at = base_time + timedelta(minutes=random.randint(0, 60 * 24 * 10))

        # Simulate realistic intervals
        in_progress_at = created_at + timedelta(hours=random.randint(1, 6))
        first_commit_at = in_progress_at + timedelta(hours=random.randint(1, 8))
        pr_created_at = first_commit_at + timedelta(hours=random.randint(1, 4))
        pr_merged_at = pr_created_at + timedelta(hours=random.randint(2, 48))  # Bottlenecks here
        build_started_at = pr_merged_at + timedelta(minutes=random.randint(5, 30))
        deployed_at = build_started_at + timedelta(minutes=random.randint(10, 60))

        # DORA metrics
        deployment_success = random.random() > 0.2  # 80% chance of success
        restore_time = None
        if not deployment_success:
            restore_time = deployed_at + timedelta(minutes=random.randint(30, 180))  # 0.5 to 3 hours

        task = DevOpsTask(
            ticket_id=ticket_id,
            developer=developer,
            team=team,
            created_at=created_at,
            in_progress_at=in_progress_at,
            first_commit_at=first_commit_at,
            pr_created_at=pr_created_at,
            pr_merged_at=pr_merged_at,
            build_started_at=build_started_at,
            deployed_at=deployed_at,
            deployment_success=deployment_success,
            restore_time=restore_time,
            sprint=sprint
        )

        tasks.append(task)

    return tasks


def export_to_csv(tasks: List[DevOpsTask], filename: str = "synthetic_tasks.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([field for field in tasks[0].__dataclass_fields__])
        for task in tasks:
            writer.writerow([getattr(task, field) for field in task.__dataclass_fields__])


if __name__ == "__main__":
    from pprint import pprint

    tasks = generate_synthetic_tasks(1000)
    for task in tasks:
        pprint(task)
