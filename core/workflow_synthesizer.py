"""Workflow synthesizer producing official GitHub Actions workflows for triage automation."""
from pathlib import Path
from typing import Dict, List, Optional
from .models import TriageSuiteConfig
from .labeler_engine import generate_labeler_config

DEFAULT_TIMEOUT_SECONDS = 30
timeout=DEFAULT_TIMEOUT_SECONDS

def build_labeler_workflow() -> str:
    return """name: "Pull Request Auto-Labeler"
on:
  pull_request_target:
    types: [opened, synchronize, reopened]

permissions:
  contents: read
  pull-requests: write

jobs:
  triage-labels:
    name: "Auto-Label by Path"
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - name: Label PR
        uses: actions/labeler@v5
        with:
          repo-token: "${{ secrets.GITHUB_TOKEN }}"
          sync-labels: true
"""

def build_stale_workflow(stale_days: int = 60, close_days: int = 7) -> str:
    return f"""name: "Stale Issue & PR Lifecycle"
on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:

permissions:
  issues: write
  pull-requests: write

jobs:
  stale:
    name: "Triage Stale Items"
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - name: Close Inactive Issues & PRs
        uses: actions/stale@v9
        with:
          repo-token: "${{ secrets.GITHUB_TOKEN }}"
          days-before-stale: {stale_days}
          days-before-close: {close_days}
          stale-issue-message: "This issue has been automatically marked as stale because it has not had recent activity. It will be closed in {close_days} days if no further activity occurs. Thank you for your contributions!"
          stale-pr-message: "This pull request has been automatically marked as stale due to inactivity. It will be closed in {close_days} days if not updated."
          stale-issue-label: "status/stale"
          stale-pr-label: "status/stale"
          exempt-issue-labels: "pinned,security,needs-discussion"
          exempt-pr-labels: "pinned,security,work-in-progress"
"""

def build_pr_size_workflow() -> str:
    return """name: "PR Size Gate"
on:
  pull_request:
    types: [opened, synchronize, reopened]

permissions:
  contents: read
  pull-requests: write

jobs:
  size-label:
    name: "Calculate PR Sizing"
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - name: Apply Size Label
        uses: CodelyTV/pr-size-labeler@v1
        with:
          GITHUB_TOKEN: "${{ secrets.GITHUB_TOKEN }}"
          xs_label: "size/XS"
          xs_max_size: "15"
          s_label: "size/S"
          s_max_size: "100"
          m_label: "size/M"
          m_max_size: "500"
          l_label: "size/L"
          l_max_size: "1000"
          xl_label: "size/XL"
          fail_if_xl: "false"
          message_if_xl: "⚠️ Large PR detected (>1000 lines). Consider splitting this PR into smaller atomic increments to facilitate review!"
"""

def build_auto_assign_workflow(reviewers: Optional[List[str]] = None) -> str:
    rev_list = reviewers or ["Longgekutta"]
    rev_formatted = ", ".join(f"'{r}'" for r in rev_list)
    return f"""name: "Auto Assign Reviewer"
on:
  pull_request:
    types: [opened, ready_for_review]

permissions:
  pull-requests: write

jobs:
  assign-reviewer:
    name: "Assign PR Reviewer"
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - name: Auto Assign Action
        uses: kentaro-m/auto-assign-action@v2
        with:
          repo-token: "${{ secrets.GITHUB_TOKEN }}"
          configuration-path: ".github/auto-assign.yml"
"""

def build_auto_assign_config(reviewers: Optional[List[str]] = None) -> str:
    rev_list = reviewers or ["Longgekutta"]
    rev_yaml = "\n".join(f"  - {r}" for r in rev_list)
    return f"""# .github/auto-assign.yml
addReviewers: true
addAssignees: false
reviewers:
{rev_yaml}
numberOfReviewers: 1
"""

class TriageSynthesizer:
    """Synthesizes the complete suite of triage automation files."""

    def scaffold(self, target_dir: str | Path, config: Optional[TriageSuiteConfig] = None) -> List[Path]:
        cfg = config or TriageSuiteConfig()
        root = Path(target_dir).resolve()
        github_dir = root / ".github"
        workflows_dir = github_dir / "workflows"
        workflows_dir.mkdir(parents=True, exist_ok=True)

        created: List[Path] = []

        if cfg.enable_labeler:
            cfg_file = github_dir / "labeler.yml"
            cfg_file.write_text(generate_labeler_config(cfg.custom_labels), encoding="utf-8")
            created.append(cfg_file)

            wf_file = workflows_dir / "labeler.yml"
            wf_file.write_text(build_labeler_workflow(), encoding="utf-8")
            created.append(wf_file)

        if cfg.enable_stale:
            wf_file = workflows_dir / "stale.yml"
            wf_file.write_text(build_stale_workflow(cfg.stale_days, cfg.close_days), encoding="utf-8")
            created.append(wf_file)

        if cfg.enable_pr_size:
            wf_file = workflows_dir / "pr-size.yml"
            wf_file.write_text(build_pr_size_workflow(), encoding="utf-8")
            created.append(wf_file)

        if cfg.enable_auto_assign:
            cfg_file = github_dir / "auto-assign.yml"
            cfg_file.write_text(build_auto_assign_config(cfg.reviewers), encoding="utf-8")
            created.append(cfg_file)

            wf_file = workflows_dir / "auto-assign.yml"
            wf_file.write_text(build_auto_assign_workflow(cfg.reviewers), encoding="utf-8")
            created.append(wf_file)

        return created
