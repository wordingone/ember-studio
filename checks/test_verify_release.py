#!/usr/bin/env python3
"""Deliberate reds for checks/verify_release.py: each broken release must fail, and the clean one must pass."""
import hashlib
import io
import os
import struct
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import verify_release  # noqa: E402


def fake_exe(subsystem=2, extra=b""):
    """A minimal PE header (DOS stub + PE signature + optional header) with the given subsystem, then `extra`."""
    data = bytearray(512)
    data[0:2] = b"MZ"
    struct.pack_into("<I", data, 0x3C, 0x80)
    data[0x80:0x84] = b"PE\0\0"
    struct.pack_into("<H", data, 0x80 + 24, 0x20B)
    struct.pack_into("<H", data, 0x80 + 24 + 68, subsystem)
    return bytes(data) + extra


def release(files, sums_override=None, zipped=None):
    """Writes a release folder: files {name: bytes}, zipped {zip name: {inner name: bytes}}; returns (folder, TemporaryDirectory)."""
    tmp = tempfile.TemporaryDirectory()
    all_files = dict(files)
    for zname, inner in (zipped or {}).items():
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as z:
            for n, b in inner.items():
                z.writestr(n, b)
        all_files[zname] = buf.getvalue()
    lines = []
    for n, b in all_files.items():
        with open(os.path.join(tmp.name, n), "wb") as fh:
            fh.write(b)
        lines.append("%s  %s" % (hashlib.sha256(b).hexdigest(), n))
    sums = sums_override(lines) if sums_override else lines
    with open(os.path.join(tmp.name, "SHA256SUMS.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(sums) + "\n")
    return tmp.name, tmp


def verdict(folder):
    import contextlib
    with contextlib.redirect_stdout(io.StringIO()) as out:
        rc = verify_release.main(folder)
    return rc, out.getvalue()


def main():
    results = []

    def expect(label, rc_want, needle, folder_tmp):
        folder, tmp = folder_tmp
        rc, out = verdict(folder)
        ok = rc == rc_want and (needle is None or needle in out)
        results.append(ok)
        print(("PASS " if ok else "FAIL ") + label + ("" if ok else " (rc=%d out=%r)" % (rc, out)))
        tmp.cleanup()

    expect("clean release passes", 0, None, release({"ember-studio-1.exe": fake_exe()}))
    expect("clean zip passes", 0, None, release({}, zipped={"ember-studio-1.zip": {"ember-studio.exe": fake_exe(), "README.md": b"x"}}))
    bad_hash = release({"ember-studio-1.exe": fake_exe()}, sums_override=lambda l: [("0" * 64) + l[0][64:]])
    expect("red: a wrong checksum", 1, "SHA-256 differs", bad_hash)
    expect("red: a file missing from the checksum list", 1, "not listed", release({"ember-studio-1.exe": fake_exe(), "ember-lab-1.exe": fake_exe()}, sums_override=lambda l: l[:1]))
    bs = chr(92)
    expect("red: a Users path in a program (ASCII)", 1, "a Users path", release({"ember-lab-1.exe": fake_exe(extra=("panic at C:" + bs + "Users" + bs + "someone").encode())}))
    expect("red: a Users path in a program (UTF-16)", 1, "UTF-16", release({"ember-lab-1.exe": fake_exe(extra=("C:" + bs + "Users" + bs + "x").encode("utf-16-le"))}))
    expect("red: a cargo folder inside a zip", 1, "cargo or rustup", release({}, zipped={"a.zip": {"ember-lab.exe": fake_exe(extra=b"/home/x/.cargo/registry")}}))
    expect("red: a console program named ember-studio", 1, "not a GUI program", release({"ember-studio-1.exe": fake_exe(subsystem=3)}))
    expect("red: a path that leaves the zip folder", 1, "leaves the folder", release({}, zipped={"a.zip": {"../evil.exe": fake_exe()}}))
    if all(results):
        print("release verifier reds passed: %d checks" % len(results))
        return 0
    print("release verifier reds FAILED")
    return 1


if __name__ == "__main__":
    sys.exit(main())
