#!/usr/bin/env python3
"""Ask Ember Studio whether a job could start, without starting it.

usage: python check_job_start.py PATH_TO_EMBER_STUDIO_EXE --script PATH --sha256 HEX --log PATH [--kind hour|learn]

It runs `ember-studio press ... --check --json`, which runs only the preflight: nothing
is started and no job file is written. It prints each check of the "Before it starts" list
(`ok`, `refused` or `unknown`; unknown blocks like refused) and exits 0 only when the job
could start. Exit codes of press: 0 can start, 2 refused, 3 bad arguments, 4 failed.
"""
import argparse
import json
import subprocess
import sys

CREATE_NO_WINDOW = 0x08000000 if sys.platform == "win32" else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("exe")
    ap.add_argument("--script", required=True)
    ap.add_argument("--sha256", required=True)
    ap.add_argument("--log", required=True)
    ap.add_argument("--kind", choices=["hour", "learn"])
    args = ap.parse_args()

    cmd = [args.exe, "press", "--script", args.script, "--sha256", args.sha256, "--log", args.log, "--check", "--json"]
    if args.kind:
        cmd += ["--kind", args.kind]
    done = subprocess.run(cmd, capture_output=True, text=True, timeout=120, creationflags=CREATE_NO_WINDOW)
    try:
        doc = json.loads(done.stdout)
    except ValueError:
        sys.stderr.write("press exited %d and printed no JSON\n%s" % (done.returncode, done.stderr))
        return done.returncode or 4
    for row in doc.get("preflight", {}).get("rows", []):
        check = row["check"]
        print("%-8s %s  %s" % (check["state"], row["label"], check.get("detail", "")))
    print("can_start: %s" % doc.get("can_start"))
    return 0 if doc.get("can_start") else (done.returncode or 2)


if __name__ == "__main__":
    sys.exit(main())
