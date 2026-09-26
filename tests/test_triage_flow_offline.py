"""Hermetic offline unit tests for tool-triage-flow-automator."""
import tempfile
import unittest
from pathlib import Path

from core.labeler_engine import generate_labeler_config, DEFAULT_LABEL_RULES
from core.workflow_synthesizer import (
    build_labeler_workflow,
    build_stale_workflow,
    build_pr_size_workflow,
    build_auto_assign_workflow,
    TriageSynthesizer
)
from core.simulator import TriageSimulator
from core.validator import TriageValidator

DEFAULT_TIMEOUT_SECONDS = 30
timeout=DEFAULT_TIMEOUT_SECONDS

class TestTriageFlowOffline(unittest.TestCase):
    def test_01_labeler_config_generation(self):
        cfg = generate_labeler_config()
        self.assertIn("documentation:", cfg)
        self.assertIn("backend:", cfg)
        self.assertIn("ci-cd:", cfg)
        self.assertIn("any-glob-to-any-file:", cfg)

    def test_02_workflow_templates(self):
        wf_labeler = build_labeler_workflow()
        self.assertIn("actions/labeler@v5", wf_labeler)
        self.assertIn("pull-requests: write", wf_labeler)

        wf_stale = build_stale_workflow(stale_days=45, close_days=5)
        self.assertIn("actions/stale@v9", wf_stale)
        self.assertIn("days-before-stale: 45", wf_stale)
        self.assertIn("days-before-close: 5", wf_stale)

        wf_size = build_pr_size_workflow()
        self.assertIn("CodelyTV/pr-size-labeler@v1", wf_size)
        self.assertIn("size/XS", wf_size)

        wf_assign = build_auto_assign_workflow(["alice", "bob"])
        self.assertIn("kentaro-m/auto-assign-action@v2", wf_assign)

    def test_03_simulator_matching(self):
        sim = TriageSimulator()
        res = sim.simulate(["docs/architecture.md", "core/main.py", "unknown/something.xyz"])
        self.assertIn("documentation", res.matched_labels)
        self.assertIn("backend", res.matched_labels)
        self.assertIn("unknown/something.xyz", res.unmatched_files)
        self.assertEqual(res.evaluated_files_count, 3)

    def test_04_synthesizer_and_validator(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            synth = TriageSynthesizer()
            created = synth.scaffold(tmp)
            self.assertGreaterEqual(len(created), 4)

            val = TriageValidator()
            rep = val.validate_repository(tmp)
            self.assertTrue(rep.is_valid)
            self.assertEqual(rep.score, 100)

if __name__ == "__main__":
    unittest.main()
