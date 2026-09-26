"""Core models for tool-triage-flow-automator."""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

DEFAULT_TIMEOUT_SECONDS = 30
timeout=DEFAULT_TIMEOUT_SECONDS

@dataclass
class LabelMatcher:
    label: str
    patterns: List[str]

@dataclass
class TriageSuiteConfig:
    enable_labeler: bool = True
    enable_stale: bool = True
    enable_pr_size: bool = True
    enable_auto_assign: bool = True
    stale_days: int = 60
    close_days: int = 7
    reviewers: List[str] = field(default_factory=list)
    custom_labels: Dict[str, List[str]] = field(default_factory=dict)

@dataclass
class SimulationResult:
    matched_labels: List[str]
    evaluated_files_count: int
    unmatched_files: List[str]

@dataclass
class TriageValidationIssue:
    severity: str  # 'ERROR', 'WARN', 'INFO'
    code: str
    message: str

@dataclass
class TriageValidationReport:
    is_valid: bool
    score: int
    issues: List[TriageValidationIssue] = field(default_factory=list)
