#!/usr/bin/env python3
"""Checks for the documentation of this repository. Exit 0 = pass, 1 = at least one failure.

(a) every relative link and image path in README.md and docs/**/*.md resolves to a file;
(b) every media file a document references exists and is under 10 MB;
(c) refusals: drive paths of a build machine, a session-link trailer, and the private
    repository's address (the product name "ember-lab" is fine; its repository path is not).

Usage: python scripts/check_docs.py [repo_root]
"""
import os
import re
import sys

MAX_MEDIA_BYTES = 10 * 1024 * 1024
MEDIA_EXT = {".png", ".jpg", ".jpeg", ".gif", ".mp4", ".webm", ".svg"}
LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HTML_SRC = re.compile(r"""(?:src|href)=["']([^"']+)["']""")

BS = chr(92) * 2  # a literal backslash inside a regex character class
REFUSALS = [
    ("a drive path of a build machine", re.compile(r"(?<![A-Za-z0-9])[A-C]:[/" + BS + r"](?!/)[A-Za-z0-9_.-]+")),
    ("a Users path of a build machine", re.compile(r"[A-Za-z]:[/" + BS + r"]Users[/" + BS + r"]")),
    ("a WSL mount path", re.compile(r"/mnt/[a-z]/")),
    ("a session-link trailer", re.compile(r"Claude-Session\s*:", re.I)),
    ("the private repository's address", re.compile(r"wordingone/ember" + r"-lab\b", re.I)),
]


def doc_files(root):
    out = []
    readme = os.path.join(root, "README.md")
    if os.path.isfile(readme):
        out.append(readme)
    for base, _dirs, files in os.walk(os.path.join(root, "docs")):
        for f in files:
            if f.endswith(".md"):
                out.append(os.path.join(base, f))
    return sorted(out)


def main(root):
    fails = []
    docs = doc_files(root)
    if not docs:
        fails.append("no README.md or docs/*.md found under " + root)
    for path in docs:
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        for lineno, line in enumerate(text.splitlines(), 1):
            for label, pat in REFUSALS:
                if pat.search(line):
                    fails.append("%s:%d: %s" % (rel, lineno, label))
        targets = LINK.findall(text) + HTML_SRC.findall(text)
        for tgt in targets:
            if re.match(r"^[a-z][a-z0-9+.-]*:", tgt, re.I) or tgt.startswith("#"):
                continue
            file_part = tgt.split("#", 1)[0].split("?", 1)[0]
            if not file_part:
                continue
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), file_part))
            if not os.path.exists(resolved):
                fails.append("%s: link does not resolve: %s" % (rel, tgt))
                continue
            if os.path.splitext(resolved)[1].lower() in MEDIA_EXT:
                size = os.path.getsize(resolved)
                if size > MAX_MEDIA_BYTES:
                    fails.append("%s: media over 10 MB (%d bytes): %s" % (rel, size, tgt))
    media_root = os.path.join(root, "docs", "media")
    if os.path.isdir(media_root):
        for f in sorted(os.listdir(media_root)):
            p = os.path.join(media_root, f)
            if os.path.splitext(f)[1].lower() in MEDIA_EXT and os.path.getsize(p) > MAX_MEDIA_BYTES:
                fails.append("docs/media/%s: over 10 MB" % f)
    if fails:
        print("docs check FAILED (%d):" % len(fails))
        for f in fails:
            print("  " + f)
        return 1
    print("docs check passed: %d documents" % len(docs))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
