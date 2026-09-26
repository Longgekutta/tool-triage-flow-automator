"""Validator for triage workflows and labeler configurations."""
from pathlib import Path
from typing import List, Dict, Any
from .models import TriageValidationReport, TriageValidationIssue

DEFAULT_TIMEOUT_SECONDS = 30
timeout=DEFAULT_TIMEOUT_SECONDS

class TriageValidator:
    """Validates triage workflows and .github/labeler.yml configurations."""

    def validate_repository(self, target_dir: str | Path) -> TriageValidationReport:
        root = Path(target_dir).resolve()
        github_dir = root / ".github"
        workflows_dir = github_dir / "workflows"

        issues: List[TriageValidationIssue] = []
        score = 100

        labeler_cfg = github_dir / "labeler.yml"
        labeler_wf = workflows_dir / "labeler.yml"
        stale_wf = workflows_dir / "stale.yml"
        pr_size_wf = workflows_dir / "pr-size.yml"

        if not labeler_cfg.is_file():
            issues.append(TriageValidationIssue(severity="WARN", code="MISSING_LABELER_CONFIG", message="Missing .github/labeler.yml: PRs will not be auto-labeled."))
            score -= 20
        else:
            try:
                content = labeler_cfg.read_text(encoding="utf-8")
                if not content.strip():
                    issues.append(TriageValidationIssue(severity="ERROR", code="EMPTY_LABELER_CONFIG", message=".github/labeler.yml is empty."))
                    score -= 25
            except Exception as e:
                issues.append(TriageValidationIssue(severity="ERROR", code="LABELER_READ_ERROR", message=f"Failed to read labeler.yml: {e}"))
                score -= 30

        if not labeler_wf.is_file():
            issues.append(TriageValidationIssue(severity="WARN", code="MISSING_LABELER_WORKFLOW", message="Missing .github/workflows/labeler.yml."))
            score -= 15
        else:
            content = labeler_wf.read_text(encoding="utf-8", errors="ignore")
            if "pull-requests: write" not in content and "permissions:" in content:
                issues.append(TriageValidationIssue(severity="ERROR", code="INSUFFICIENT_PERMISSIONS", message="labeler.yml missing 'pull-requests: write' permission."))
                score -= 25

        if not stale_wf.is_file():
            issues.append(TriageValidationIssue(severity="INFO", code="MISSING_STALE_WORKFLOW", message="Missing .github/workflows/stale.yml (inactive issues won't be triaged)."))
            score -= 10

        if not pr_size_wf.is_file():
            issues.append(TriageValidationIssue(severity="INFO", code="MISSING_PR_SIZE_WORKFLOW", message="Missing .github/workflows/pr-size.yml (PR sizes not gated)."))
            score -= 10

        score = max(0, min(100, score))
        is_valid = not any(i.severity == "ERROR" for i in issues)

        return TriageValidationReport(
            is_valid=is_valid,
            score=score,
            issues=issues
        )
