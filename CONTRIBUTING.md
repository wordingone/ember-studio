# Contributing

Thank you for looking. This repository is the public face of Ember Studio, so what you can change here is limited on purpose.

## What a pull request here can change

- the documentation under `docs/` (a manual fix, a clearer sentence, a correction with the build it was checked against);
- file format pages, schemas and their examples under `docs/formats/`;
- job kind manifests under `manifests/kinds/` and experiment manifests under `manifests/experiments/`;
- example agent scripts under `examples/agents/` and example experiments under `examples/experiments/`;
- themes under `themes/`;
- the checks under `checks/`.

## What it cannot change

- **The program's behaviour.** Its source is in a private repository. A pull request that adds Rust, a Cargo manifest or Python that is not a check or an example agent script is closed; `python checks/allowlist.py` fails on it and names the path.
- `docs/interface/`. It is generated from the program by its release process. Open an issue describing the change you want.

If a bug is in the program, open an issue (below). Do not try to fix it here.

## Before you open a pull request

1. Run `python checks/run_all.py`. It needs Python 3.10 or later and the `jsonschema` package. It must print `all checks passed`.
2. Every statement you add about the program must be true of the latest release, or say which build you checked it against. If you could not check it, say so in the text.
3. No personal names, no secrets, no folder paths of your machine (use placeholders such as `<folder>` and variables such as `%LOCALAPPDATA%`).
4. An example runs on a small open model, names the model and its licence, finishes in under ten minutes on a consumer card and uses only documented commands.
5. Keep a pull request to one purpose. A move of a file and a change of its text go in separate commits.

## Opening an issue

Use the forms. A useful bug report has the build or release id, the steps, the receipt or log file the program wrote (remove anything private) and a picture of the window. [Known limits](docs/known-limits.md) lists what is already known to be missing.

## Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Security reports: see [SECURITY.md](SECURITY.md).
