from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class DevOpsTask:
    # Basic metadata
    ticket_id: str
    developer: str
    team: str

    # Workflow timestamps
    created_at: datetime                    # Ticket created
    in_progress_at: datetime                # Moved to in progress
    first_commit_at: datetime               # First code commit
    pr_created_at: datetime                 # PR opened
    pr_merged_at: datetime                  # PR merged
    build_started_at: datetime              # Build started
    deployed_at: datetime                   # Production deployment
    deployment_success: bool = True
    restore_time: Optional[datetime] = None
    pr_lines_changed: Optional[int] = None
    test_passed: Optional[bool] = True
    deployment_successful: Optional[bool] = True
    incident_reported: Optional[bool] = False

