"""The maintainer's gate on a fork's pull request agrees with `book audit` on what fails."""
import json
import subprocess
import sys
from pathlib import Path

from bookkit import audit

GATE = Path(__file__).resolve().parents[1] / "layout_gate.py"
FINDINGS = [
    [],
    [{"check": "word-gap", "severity": "warning", "detail": "-", "baselined": True}],
    [{"check": "hole", "severity": "warning", "detail": "-"}],
    [{"check": "version", "severity": "error", "detail": "-"}],
]


def test_the_gate_fails_exactly_where_the_strict_audit_does(tmp_path):
    for findings in FINDINGS:
        report = tmp_path / "audit.json"
        report.write_text(json.dumps({"findings": findings}), encoding="utf-8")
        gate = subprocess.run([sys.executable, str(GATE), str(report)], capture_output=True, text=True)
        assert (gate.returncode == 1) == audit.failed(findings), (findings, gate.stdout)
