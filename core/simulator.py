"""Offline triage simulator predicting labels for given changed files."""
import fnmatch
from pathlib import Path
from typing import List, Dict
from .models import SimulationResult
from .labeler_engine import DEFAULT_LABEL_RULES

DEFAULT_TIMEOUT_SECONDS = 30
timeout=DEFAULT_TIMEOUT_SECONDS

class TriageSimulator:
    """Simulates path matching against labeler rules."""

    def __init__(self, rules: Dict[str, List[str]] = None):
        self.rules = rules or DEFAULT_LABEL_RULES

    def match_file(self, file_path: str, pattern: str) -> bool:
        # Normalize paths
        norm_path = file_path.replace("\\", "/")
        norm_pat = pattern.replace("\\", "/")

        if norm_pat.startswith("**/"):
            base_pat = norm_pat[3:]
            if fnmatch.fnmatch(norm_path, base_pat) or fnmatch.fnmatch(norm_path.split("/")[-1], base_pat):
                return True

        if norm_pat.endswith("/**"):
            prefix = norm_pat[:-3]
            if norm_path.startswith(prefix + "/") or norm_path == prefix:
                return True

        return fnmatch.fnmatch(norm_path, norm_pat)

    def simulate(self, changed_files: List[str]) -> SimulationResult:
        matched = set()
        unmatched = []

        for f in changed_files:
            file_matched = False
            for label, patterns in self.rules.items():
                for pat in patterns:
                    if self.match_file(f, pat):
                        matched.add(label)
                        file_matched = True
                        break
            if not file_matched:
                unmatched.append(f)

        return SimulationResult(
            matched_labels=sorted(list(matched)),
            evaluated_files_count=len(changed_files),
            unmatched_files=unmatched
        )
