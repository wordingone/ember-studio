#!/usr/bin/env python3
"""Deliberate reds for check_docs.py: each broken tree must fail, and the clean tree must pass."""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHECK = os.path.join(HERE, "check_docs.py")
BS = chr(92)


def make_tree(root, readme, extra=None, big=False):
    os.makedirs(os.path.join(root, "docs", "media"))
    with open(os.path.join(root, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme)
    with open(os.path.join(root, "docs", "media", "ok.png"), "wb") as f:
        f.write(b"x" * 10)
    if big:
        with open(os.path.join(root, "docs", "media", "big.mp4"), "wb") as f:
            f.truncate(10 * 1024 * 1024 + 1)
    for name, text in (extra or {}).items():
        with open(os.path.join(root, name), "w", encoding="utf-8") as f:
            f.write(text)


def run(root):
    p = subprocess.run([sys.executable, CHECK, root], capture_output=True, text=True)
    return p.returncode, p.stdout


CASES = [
    ("clean tree passes", "See [a](docs/a.md) ![x](docs/media/ok.png)\n", {"docs/a.md": "ok\n"}, False, 0),
    ("broken relative link fails", "See [a](docs/missing.md)\n", {}, False, 1),
    ("missing image fails", "![x](docs/media/nope.png)\n", {}, False, 1),
    ("media over 10 MB fails", "![x](docs/media/ok.png)\n", {}, True, 1),
    ("build-machine drive path fails", "Path B:/some/dir here\n", {}, False, 1),
    ("Users path fails", "Path C:" + BS + "Users" + BS + "someone here\n", {}, False, 1),
    ("session trailer fails", "Claude-Session: https://example.invalid/x\n", {}, False, 1),
    ("private repository address fails", "git clone wordingone/ember" + "-lab\n", {}, False, 1),
    ("product name alone passes", "ember-lab is the daemon.\n", {}, False, 0),
]


def main():
    bad = 0
    for name, readme, extra, big, want in CASES:
        with tempfile.TemporaryDirectory() as root:
            make_tree(root, readme, extra, big)
            rc, out = run(root)
        ok = rc == want
        print(("ok   " if ok else "FAIL ") + name + " (exit %d, wanted %d)" % (rc, want))
        bad += 0 if ok else 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
