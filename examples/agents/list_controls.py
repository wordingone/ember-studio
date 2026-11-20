#!/usr/bin/env python3
"""List the controls of an Ember Studio tab by name, role and state.

usage: python list_controls.py PATH_TO_EMBER_STUDIO_EXE [--mode SLUG] [--role ROLE]

It runs `ember-studio ui-tree --json`, which draws a fresh window offscreen and prints
every control. It opens no window, takes no focus and does not touch a running Studio.
Output: one line per control, `<role>  <name>  [disabled]  = <value>`, then a count.
"""
import argparse
import json
import subprocess
import sys

CREATE_NO_WINDOW = 0x08000000 if sys.platform == "win32" else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("exe", help="path of the ember-studio program")
    ap.add_argument("--mode", help="tab slug to draw (default: the program's default tab)")
    ap.add_argument("--role", help="only controls of this role, for example Button or TextInput")
    args = ap.parse_args()

    cmd = [args.exe, "ui-tree", "--json"]
    if args.mode:
        cmd += ["--mode", args.mode]
    done = subprocess.run(cmd, capture_output=True, text=True, timeout=120, creationflags=CREATE_NO_WINDOW)
    if done.returncode != 0:
        sys.stderr.write("ui-tree exited %d\n%s" % (done.returncode, done.stderr))
        return done.returncode
    tree = json.loads(done.stdout)
    shown = 0
    for item in tree:
        if args.role and item["role"] != args.role:
            continue
        shown += 1
        flag = "  [disabled]" if item["disabled"] else ""
        value = "" if item["value"] is None else "  = " + item["value"]
        print("%-18s %s%s%s" % (item["role"], item["name"], flag, value))
    print("%d controls" % shown)
    return 0


if __name__ == "__main__":
    sys.exit(main())
