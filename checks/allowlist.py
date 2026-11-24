#!/usr/bin/env python3
"""The allow-list check for this repository. Exit 0 = pass, 1 = at least one failure.

This repository is the public face of Ember Studio: documentation, file formats, manifests,
examples and the checks that guard them. It holds no source of the program. This check lists
every tracked path and fails when a path is not allowed, naming the path. Its clauses:

  1. every tracked path matches an allow-list pattern (the number of paths that match no rule
     is printed as `unmatched` and must be 0);
  2. no program source: no .rs file, no Cargo.toml or Cargo.lock, and no .py file outside
     checks/ and examples/agents/;
  3. no built program, debug symbol or compiled file: .exe .dll .pdb .so .dylib .zip .msi .pyc (builds are published on the
     Releases page, never kept in the tree);
  4. no name of an internal package of the program in any text file outside docs/interface/
     (the list is PRIVATE_NAMES below);
  5. no folder path of a build machine (a drive letter path, a user-profile path, a WSL mount)
     and no session-link trailer in any text file.

Usage: python checks/allowlist.py [repo_root]    (default: the current folder)
       python checks/allowlist.py --paths FILE   (read the path list from FILE instead of git)
"""
import fnmatch
import os
import re
import subprocess
import sys

ALLOW = [
    "README.md", "CHANGELOG.md", "ROADMAP.md", "LICENSE", "NOTICE", "TERMS-RELEASED-BUILDS.md",
    "CONTRIBUTING.md", "AGENTS.md", "CLAUDE.md", "SECURITY.md", "CODE_OF_CONDUCT.md",
    ".gitignore", ".gitattributes",
    "docs/**", "manifests/**", "examples/**", "themes/**", "checks/**",
    ".github/ISSUE_TEMPLATE/**", ".github/pull_request_template.md", ".github/workflows/**",
]
SOURCE_EXT = {".rs"}
SOURCE_NAMES = {"Cargo.toml", "Cargo.lock"}
PYTHON_OK = ("checks/", "examples/agents/")
BINARY_EXT = {".exe", ".dll", ".pdb", ".so", ".dylib", ".zip", ".msi", ".lib", ".obj", ".pyc"}
TEXT_EXT = {".md", ".txt", ".json", ".yml", ".yaml", ".toml", ".py", ".ps1", ".sh", ".ember", ".html", ".csv", ".css", ".svg", ""}
# Internal package names of the program. A hit outside docs/interface/ means the text describes the
# program's internals instead of its public interface. Kept in step with the program's workspace by
# the release pipeline.
PRIVATE_NAMES = [
    "ember-contract", "ember-platform", "ember-data", "ember-pipe", "ember-jobs", "ember-model",
    "ember-agent", "ember-ops", "ember-studio-kit", "ember-studio-client", "ember-studio-pages",
    "ember-studio-tabs", "ember-devhost", "ember_contract", "ember_platform", "ember_jobs",
    "ember_agent", "ember_ops", "ember_studio_kit", "ember_studio_client", "ember_studio_pages",
    "ember_studio_tabs", "cargo xtask",
]
BS = chr(92) * 2
PATH_REFUSALS = [
    ("a drive path of a build machine", re.compile(r"(?<![A-Za-z0-9])[A-C]:[/" + BS + r"](?!/)[A-Za-z0-9_.-]+")),
    ("a Users path of a build machine", re.compile(r"[A-Za-z]:[/" + BS + r"]Users[/" + BS + r"]")),
    ("a WSL mount path", re.compile(r"/mnt/[a-z]/")),
    ("a session-link trailer", re.compile(r"Claude-Session\s*:", re.I)),
]
NAME_RE = re.compile("|".join(re.escape(n) for n in PRIVATE_NAMES))


def matches(path, pattern):
    if pattern.endswith("/**"):
        return path.startswith(pattern[:-2])
    return fnmatch.fnmatchcase(path, pattern)


def tracked(root, paths_file=None):
    if paths_file:
        with open(paths_file, encoding="utf-8") as fh:
            return [l.strip() for l in fh if l.strip()]
    out = subprocess.run(["git", "-C", root, "ls-files", "-z"], capture_output=True, check=True).stdout
    return [p for p in out.decode("utf-8").split("\0") if p]


def check(root, paths):
    fails = []
    unmatched = 0
    for p in paths:
        ext = os.path.splitext(p)[1].lower()
        base = os.path.basename(p)
        if not any(matches(p, pat) for pat in ALLOW):
            unmatched += 1
            fails.append("%s: matches no allow-list rule" % p)
            continue
        if ext in SOURCE_EXT or base in SOURCE_NAMES:
            fails.append("%s: program source is not kept in this repository" % p)
        if ext == ".py" and not p.startswith(PYTHON_OK):
            fails.append("%s: a Python file outside checks/ and examples/agents/" % p)
        if ext in BINARY_EXT:
            fails.append("%s: a built program or debug symbol; builds go on the Releases page" % p)
    for p in paths:
        ext = os.path.splitext(p)[1].lower()
        full = os.path.join(root, p)
        if ext not in TEXT_EXT or not os.path.isfile(full):
            continue
        try:
            with open(full, encoding="utf-8") as fh:
                text = fh.read()
        except (UnicodeDecodeError, OSError):
            continue
        if p.startswith("checks/test_"):
            continue  # the deliberate reds hold the very strings the clauses refuse
        for n, line in enumerate(text.splitlines(), 1):
            for label, pat in PATH_REFUSALS:
                if pat.search(line):
                    fails.append("%s:%d: %s" % (p, n, label))
            if not p.startswith("docs/interface/") and not p.startswith("checks/"):
                m = NAME_RE.search(line)
                if m:
                    fails.append("%s:%d: names an internal package of the program (%s)" % (p, n, m.group(0)))
    return fails, unmatched


def main(argv):
    paths_file = None
    args = list(argv)
    if args[:1] == ["--paths"]:
        paths_file = args[1]
        args = args[2:]
    root = args[0] if args else "."
    paths = tracked(root, paths_file)
    fails, unmatched = check(root, paths)
    print("allowlist: %d paths, unmatched %d" % (len(paths), unmatched))
    if fails:
        print("allowlist FAILED (%d):" % len(fails))
        for f in fails:
            print("  " + f)
        return 1
    print("allowlist passed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
