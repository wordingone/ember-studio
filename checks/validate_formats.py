#!/usr/bin/env python3
"""Validates every schema of the public working copy against its examples, and proves each schema refuses a broken one.

usage: python validate_formats.py <public working copy>
Prints one line per check and a count; exits 1 on any failure.
"""
import copy
import glob
import json
import os
import sys

from jsonschema import Draft202012Validator

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
F = os.path.join(ROOT, "docs", "formats")
ok = bad = 0


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def check(label, cond):
    global ok, bad
    if cond:
        ok += 1
        print("PASS " + label)
    else:
        bad += 1
        print("FAIL " + label)


def valid(validator, doc):
    return not list(validator.iter_errors(doc))


def val(name):
    schema = load(os.path.join(F, name + ".schema.json"))
    Draft202012Validator.check_schema(schema)
    check(name + ".schema.json is a valid draft 2020-12 schema", True)
    return Draft202012Validator(schema)


def ex(name):
    return load(os.path.join(F, "examples", name))


# job receipt: five variants, each example valid; each broken copy refused
v = val("job-receipt")
variants = {
    "job-receipt.example.json": [("state not a job state", lambda d: d.__setitem__("state", "done")), ("extra member", lambda d: d.__setitem__("x", 1))],
    "job-receipt.start.example.json": [("kind unknown", lambda d: d.__setitem__("kind", "pretrain")), ("started phase without pid", lambda d: d.pop("pid"))],
    "job-receipt.inspect-intent.example.json": [("grid over 64", lambda d: d["request"].__setitem__("grid", 65)), ("lease is the card lease", lambda d: d.__setitem__("lease", "hour-chain"))],
    "job-receipt.inspect-terminal.example.json": [("published without result", lambda d: d.pop("result")), ("outcome unknown", lambda d: d.__setitem__("outcome", "ok"))],
    "job-receipt.press-refused.example.json": [("event unknown", lambda d: d.__setitem__("event", "pressed")), ("rc a word", lambda d: d.__setitem__("rc", "32"))],
}
for name, breaks in variants.items():
    doc = ex(name)
    check("example %s validates against job-receipt" % name, valid(v, doc))
    for why, fn in breaks:
        d = copy.deepcopy(doc)
        fn(d)
        check("   broken (%s) is refused" % why, not valid(v, d))

# pin set
v = val("pin-set")
doc = ex("pin-set.example.json")
check("example pin-set.example.json validates", valid(v, doc))
for why, fn in [
    ("backslash in path", lambda d: d[0].__setitem__("relative_path", "run1\\model.bin")),
    ("parent component in path", lambda d: d[0].__setitem__("relative_path", "../x.bin")),
    ("duplicate without witness", lambda d: d[1].__setitem__("duplicate_witness", None)),
    ("witness on a protected row", lambda d: d[0].__setitem__("duplicate_witness", copy.deepcopy(d[1]["duplicate_witness"]))),
    ("checkpoint on a state row", lambda d: d[2].__setitem__("checkpoint", {"series": "a", "sequence": 1})),
    ("empty pin reason", lambda d: d[0].__setitem__("pin_reasons", [" "])),
    ("class unknown", lambda d: d[0].__setitem__("class", "cache")),
    ("unknown member", lambda d: d[0].__setitem__("note", "x")),
]:
    d = copy.deepcopy(doc)
    fn(d)
    check("   broken (%s) is refused" % why, not valid(v, d))

# experiment manifest
v = val("experiment-manifest")
doc = ex("experiment-manifest.example.json")
check("example experiment-manifest.example.json validates", valid(v, doc))
for p in sorted(glob.glob(os.path.join(ROOT, "manifests", "experiments", "*.ember"))):
    check("manifests/experiments/%s validates" % os.path.basename(p), valid(v, load(p)))
for why, fn in [
    ("other schema word", lambda d: d.__setitem__("schema", "ember-research/2")),
    ("kind unknown", lambda d: d["experiments"][0].__setitem__("kind", "TRAIN")),
    ("sha256 not hex", lambda d: d["experiments"][0].__setitem__("bar_sha256", "abc")),
    ("member missing", lambda d: d.pop("receipts")),
    ("role unknown", lambda d: d["models"][0].__setitem__("role", "teacher")),
]:
    d = copy.deepcopy(doc)
    fn(d)
    check("   broken (%s) is refused" % why, not valid(v, d))

# job kind manifest
v = val("job-kind-manifest")
check("example job-kind-manifest.example.json validates", valid(v, ex("job-kind-manifest.example.json")))
kinds = sorted(glob.glob(os.path.join(ROOT, "manifests", "kinds", "*.json")))
for p in kinds:
    check("manifests/kinds/%s validates" % os.path.basename(p), valid(v, load(p)))
doc = load(kinds[0])
for why, fn in [
    ("lease class unknown", lambda d: d.__setitem__("lease_class", "gpu")),
    ("kind not in the table", lambda d: d.__setitem__("kind", "pretrain")),
    ("exit code range over 255", lambda d: d["refusal_exit_codes"].__setitem__("max", 300)),
    ("member missing", lambda d: d.pop("refusal_codes")),
]:
    d = copy.deepcopy(doc)
    fn(d)
    check("   broken (%s) is refused" % why, not valid(v, d))

# mark
v = val("mark")
doc = ex("mark.example.json")
check("example mark.example.json validates", valid(v, doc))
for why, fn in [
    ("ctx_tokens negative", lambda d: d.__setitem__("ctx_tokens", -1)),
    ("approval without decision", lambda d: d["approval"].pop("decision")),
    ("unknown key", lambda d: d.__setitem__("note", "x")),
]:
    d = copy.deepcopy(doc)
    fn(d)
    check("   broken (%s) is refused" % why, not valid(v, d))

# interface schema
v = Draft202012Validator(load(os.path.join(ROOT, "docs", "interface", "commands.schema.json")))
Draft202012Validator.check_schema(v.schema)
check("commands.schema.json is a valid draft 2020-12 schema", True)
good = [
    {"jsonrpc": "2.0", "id": 1, "method": "ping"},
    {"jsonrpc": "2.0", "id": 2, "method": "list_jobs"},
    {"jsonrpc": "2.0", "id": 3, "method": "list_jobs", "params": {"limit": 5}},
    {"jsonrpc": "2.0", "id": 4, "method": "stop_job", "params": {"job_id": "hour-x"}},
    {"jsonrpc": "2.0", "id": 5, "method": "start_lab_job", "params": {"kind": "inspect", "checkpoint": "/m/a.safetensors", "grid": 16}},
    {"jsonrpc": "2.0", "id": 6, "method": "start_lab_job", "params": {"kind": "learn", "script": "/w/learn_a.sh", "sha256": "0" * 64, "log": "/w/a.log", "env": {}, "method": "lora"}},
    {"jsonrpc": "2.0", "id": 7, "method": "agent_live_stream", "params": {"session": "s1"}},
    {"jsonrpc": "2.0", "id": 8, "method": "job_events", "params": {"job_id": "j", "after_seq": 0, "limit": 10}},
]
bad_reqs = [
    ("unknown method", {"jsonrpc": "2.0", "id": 1, "method": "start_everything"}),
    ("stop_job without job_id", {"jsonrpc": "2.0", "id": 1, "method": "stop_job", "params": {}}),
    ("stop_job without params", {"jsonrpc": "2.0", "id": 1, "method": "stop_job"}),
    ("sha256 not hex", {"jsonrpc": "2.0", "id": 1, "method": "bind_identity", "params": {"job_id": "j", "path": "/a", "sha256": "xyz"}}),
    ("inspect grid 65", {"jsonrpc": "2.0", "id": 1, "method": "start_lab_job", "params": {"kind": "inspect", "checkpoint": "/a", "grid": 65}}),
    ("ping with params", {"jsonrpc": "2.0", "id": 1, "method": "ping", "params": {"x": 1}}),
    ("wrong version", {"jsonrpc": "1.0", "id": 1, "method": "ping"}),
]
for d in good:
    check("request %s validates" % d["method"], valid(v, d))
for why, d in bad_reqs:
    check("   broken (%s) is refused" % why, not valid(v, d))
check("commands.md names all 40 verbs", all(("`%s`" % m) in open(os.path.join(ROOT, "docs", "interface", "commands.md"), encoding="utf-8").read() for m in v.schema["properties"]["method"]["enum"]))

print("%d checks passed, %d failed" % (ok, bad))
sys.exit(1 if bad else 0)
