# File formats

The files that Studio and the lab write or read, each with a page, a JSON Schema (draft 2020-12) and a small valid example. Every statement on these pages was checked against the program's source. Where a format could not be found, the page says so.

| Format | Exists in the program | Page | Schema | Example |
| --- | --- | --- | --- | --- |
| Job receipt | Yes, in five shapes: the lab's operational receipt, start receipt, inspect intent and inspect terminal receipts, and Studio's press receipt rows | [job-receipt.md](job-receipt.md) | [job-receipt.schema.json](job-receipt.schema.json) | [examples/job-receipt.example.json](examples/job-receipt.example.json) and one per other shape |
| Capture record | **No.** A job kind `capture` is in the lab's table and is not built | [capture-record.md](capture-record.md) | none | none |
| Experiment manifest | Yes, as the research project file (`.ember`, word `ember-research/1`) | [experiment-manifest.md](experiment-manifest.md) | [experiment-manifest.schema.json](experiment-manifest.schema.json) | [examples/experiment-manifest.example.json](examples/experiment-manifest.example.json) |
| Job kind manifest | **No file.** The kinds are a table compiled into the lab; the manifests here are descriptions written from it, and nothing reads them | [job-kind-manifest.md](job-kind-manifest.md) | [job-kind-manifest.schema.json](job-kind-manifest.schema.json) | [examples/job-kind-manifest.example.json](examples/job-kind-manifest.example.json) |
| Pin set | Yes, as the storage declarations file of a reconciliation | [pin-set.md](pin-set.md) | [pin-set.schema.json](pin-set.schema.json) | [examples/pin-set.example.json](examples/pin-set.example.json) |
| Mark | **No file.** The nearest is the `ember_marks` object on a message of an Agent session record | [mark.md](mark.md) | [mark.schema.json](mark.schema.json) (the object only) | [examples/mark.example.json](examples/mark.example.json) |

Related files in this repository:

- [`manifests/kinds/`](../../manifests/kinds): one manifest for each job kind the lab can run today.
- [`manifests/experiments/`](../../manifests/experiments): two experiment manifests (research project files) that open in the Research tab.
- [Command reference](../interface/commands.md) and its [schema](../interface/commands.schema.json): every command an agent or script may send.

## Validating a file

Any JSON Schema validator for draft 2020-12 works. With Python and the `jsonschema` package:

```python
import json, jsonschema
schema = json.load(open("docs/formats/pin-set.schema.json"))
jsonschema.Draft202012Validator(schema).validate(json.load(open("my-pin-set.json")))
```

A file that passes is one the program would accept in shape. The schemas hold files to what the program writes, which is stricter than what it reads in places; each page says where.
