#!/usr/bin/env python3
"""Runs every check of this repository, in order, and fails if any fails. Usage: python checks/run_all.py"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
STEPS = [
    ("allowlist", ["checks/allowlist.py", "."]),
    ("allowlist reds", ["checks/test_allowlist.py"]),
    ("docs", ["checks/check_docs.py", "."]),
    ("docs reds", ["checks/test_check_docs.py"]),
    ("formats", ["checks/validate_formats.py", "."]),
    ("release verifier reds", ["checks/test_verify_release.py"]),
]


def main():
    failed = []
    for label, argv in STEPS:
        print("== " + label)
        rc = subprocess.run([sys.executable] + argv, cwd=ROOT).returncode
        if rc != 0:
            failed.append(label)
    if failed:
        print("FAILED: " + ", ".join(failed))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
