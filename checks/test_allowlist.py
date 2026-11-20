#!/usr/bin/env python3
"""Deliberate reds for checks/allowlist.py: one broken tree per clause, each must fail, and the clean tree must pass."""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import allowlist  # noqa: E402


def run(files):
    """files: {relative path: text}. Returns (exit code of the check, its printed failures)."""
    with tempfile.TemporaryDirectory() as root:
        for rel, text in files.items():
            full = os.path.join(root, rel)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "w", encoding="utf-8") as fh:
                fh.write(text)
        fails, unmatched = allowlist.check(root, sorted(files))
        return fails, unmatched


GOOD = {
    "README.md": "# Ember Studio\n",
    "docs/lab.md": "The lab is a daemon.\n",
    "docs/interface/commands.md": "ember-agent is named here, which is allowed in the interface folder.\n",
    "examples/agents/list.py": "print('ok')\n",
    "checks/allowlist.py": "print('x')\n",
    "manifests/kinds/hour.json": "{}\n",
}


def main():
    results = []

    def red(label, files, needle):
        fails, unmatched = run(files)
        hit = any(needle in f for f in fails)
        results.append((label, hit))
        print(("PASS" if hit else "FAIL") + " red: " + label)

    fails, unmatched = run(GOOD)
    clean = not fails and unmatched == 0
    results.append(("clean tree passes with 0 unmatched", clean))
    print(("PASS" if clean else "FAIL") + " clean tree passes with 0 unmatched (fails=%r, unmatched=%d)" % (fails, unmatched))

    red("clause 1: a path no rule allows", dict(GOOD, **{"notes/todo.txt": "x"}), "matches no allow-list rule")
    red("clause 2: a Rust file", dict(GOOD, **{"docs/x.rs": "fn main() {}"}), "program source")
    red("clause 2: a Cargo manifest", dict(GOOD, **{"examples/Cargo.toml": "[package]"}), "program source")
    red("clause 2: Python outside checks and examples/agents", dict(GOOD, **{"docs/tool.py": "x=1"}), "Python file outside")
    red("clause 3: an executable", dict(GOOD, **{"docs/media/ember-studio.exe": "MZ"}), "built program")
    red("clause 3: a debug symbol file", dict(GOOD, **{"docs/media/x.pdb": "x"}), "built program")
    red("clause 4: an internal package name", dict(GOOD, **{"docs/lab.md": "see ember-jobs for more"}), "internal package")
    red("clause 5: a build machine drive path", dict(GOOD, **{"docs/lab.md": "the file is at B:/work/x"}), "drive path")
    red("clause 5: a session-link trailer", dict(GOOD, **{"CHANGELOG.md": "Claude-Session: x"}), "session-link")
    if all(ok for _, ok in results):
        print("allowlist reds passed: %d checks" % len(results))
        return 0
    print("allowlist reds FAILED")
    return 1


if __name__ == "__main__":
    sys.exit(main())
