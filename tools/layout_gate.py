"""The maintainer's gate on a pull request from a fork: fails when the audit (run with --advisory, which passes on
layout warnings) found a warning the baseline does not accept, so that main never turns red after a merge. The
contributor's own check is `audit`; this one is the maintainer's, who fixes the pages in the pull request's branch.

Standard library only: CI runs it with the runner's python3 on the audit.json of the `audit` job.
Usage: python3 tools/layout_gate.py dist/ci/audit.json"""
import json
import sys


def open_findings(report: dict) -> list[dict]:
    """The errors and the warnings the baseline does not accept - the same rule as `bookkit.audit.failed`."""
    return [f for f in report.get("findings", [])
            if f["severity"] == "error" or f["severity"] == "warning" and not f.get("baselined")]


def main(path: str) -> int:
    with open(path, encoding="utf-8") as file:
        found = open_findings(json.load(file))
    for f in found:
        print(f"p. {f.get('page', 0)}: {f['check']} - {f['detail']}")
    if found:
        print(f"{len(found)} layout finding(s): the maintainer fixes them in this branch before the merge")
        return 1
    print("layout clean")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
