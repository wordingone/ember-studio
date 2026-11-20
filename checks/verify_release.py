#!/usr/bin/env python3
"""Verifies a downloaded release: checksums, no build-machine path in a program, the Studio program is a GUI program.

Usage: python checks/verify_release.py <folder holding the release files>
The folder holds the zip(s) and/or program files of one release and a checksum file named SHA256SUMS.txt
(lines of `<sha256>  <file name>`). Exit 0 = pass, 1 = at least one failure.

Clauses:
  1. every release file (zip, exe) is listed in SHA256SUMS.txt and its SHA-256 equals the listed one;
  2. no program (a .exe, or an .exe inside a zip) holds the folder name of a build machine: a Users path or a
     cargo/rustup folder, searched as ASCII and as UTF-16LE;
  3. every program named ember-studio*.exe is a GUI program (PE subsystem 2), so no console opens with it.
"""
import hashlib
import io
import os
import re
import struct
import sys
import zipfile

SEP = b"[" + bytes([92, 92]) + b"/]"  # a regex class of one backslash (escaped) or a slash
LEAK = [
    ("a Users path", re.compile(rb"[A-Za-z]:" + SEP + b"+" + b"Users" + SEP, re.I)),
    ("a cargo or rustup folder", re.compile(SEP + rb"\.(?:cargo|rustup)" + SEP, re.I)),
    ("a registry source folder", re.compile(rb"registry" + SEP + rb"src" + SEP + rb"index\.crates\.io", re.I)),
]


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def read_sums(folder):
    path = os.path.join(folder, "SHA256SUMS.txt")
    sums = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            m = re.match(r"^([0-9a-fA-F]{64})\s+\*?(.+)$", line)
            if m:
                sums[m.group(2).strip()] = m.group(1).lower()
    return sums


def pe_subsystem(data):
    if data[:2] != b"MZ" or len(data) < 0x40:
        return None
    off = struct.unpack_from("<I", data, 0x3C)[0]
    if data[off:off + 4] != b"PE\0\0":
        return None
    return struct.unpack_from("<H", data, off + 24 + 68)[0]


def scan_program(label, data, fails):
    # UTF-16LE text of ASCII letters is the same bytes with a zero between: dropping the zeros turns it into ASCII.
    for form, blob in (("ASCII", data), ("UTF-16", data.replace(b"\0", b""))):
        for what, pat in LEAK:
            if pat.search(blob):
                fails.append("%s: holds %s (%s)" % (label, what, form))
    inner_name = label.split("!")[-1]
    if os.path.basename(inner_name).lower().startswith("ember-studio") and inner_name.lower().endswith(".exe"):
        sub = pe_subsystem(data)
        if sub != 2:
            fails.append("%s: not a GUI program (PE subsystem %r, want 2)" % (label, sub))


def programs_in_zip(label, data):
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for info in z.infolist():
            name = info.filename
            parts = name.replace(chr(92), "/").split("/")
            if name.startswith("/") or ".." in parts:
                yield label + "!" + name, None
                continue
            if name.lower().endswith(".exe"):
                yield label + "!" + name, z.read(info)


def main(folder):
    fails = []
    try:
        sums = read_sums(folder)
    except OSError:
        print("release check FAILED (1):\n  SHA256SUMS.txt is missing")
        return 1
    files = sorted(f for f in os.listdir(folder) if f.lower().endswith((".zip", ".exe")))
    if not files:
        fails.append("no zip or exe in the folder")
    for f in files:
        with open(os.path.join(folder, f), "rb") as fh:
            data = fh.read()
        if f not in sums:
            fails.append("%s: not listed in SHA256SUMS.txt" % f)
        elif sums[f] != sha256(data):
            fails.append("%s: SHA-256 differs from SHA256SUMS.txt" % f)
        if f.lower().endswith(".exe"):
            scan_program(f, data, fails)
        else:
            for label, inner in programs_in_zip(f, data):
                if inner is None:
                    fails.append("%s: a path that leaves the folder" % label)
                else:
                    scan_program(label, inner, fails)
    for name in sums:
        if name not in files:
            fails.append("%s: listed in SHA256SUMS.txt but not present" % name)
    if fails:
        print("release check FAILED (%d):" % len(fails))
        for f in fails:
            print("  " + f)
        return 1
    print("release check passed: %d file(s)" % len(files))
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
