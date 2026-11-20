# Changelog

Changes to what this repository publishes and to the program as documented here. The program has no published release yet; entries under "Unreleased" describe the documentation and the build it was checked against.

## Unreleased

### Documentation, checked against build `de6494fe` (version 0.5.0 preview)
- Added: [the five capabilities](docs/capabilities.md), [how the program is built](docs/architecture.md) (sixteen packages in three folders and the rule between them), [file formats](docs/formats/README.md) with JSON Schemas and examples, the [command reference](docs/interface/commands.md) and its schema, job kind and experiment manifests under `manifests/`, example agent scripts under `examples/agents/`.
- Added: the allow-list check (`checks/allowlist.py`), the release verifier (`checks/verify_release.py`), format validation (`checks/validate_formats.py`) and `checks/run_all.py`, each with deliberate reds.
- Added: `AGENTS.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, issue forms and a pull request template.
- Changed: the lab's folders, tools and custody drive are described as settings (`ember-lab.toml`, environment variables, `ember-lab paths`), replacing the earlier statement that they were fixed to one machine. See [lab](docs/lab.md).
- Changed: the [Agent guide](docs/tabs/agent.md) now covers the provider config file (`model`: `provider/model`), exact token counting by the model server's tokenizer, compaction of long sessions, the state line's separate prompt-read and first-token times, and the cut-reason note.
- Changed: guides for the other tabs, the window, the command line, install, platforms and troubleshooting were re-read against the current source; pictures that changed materially were redrawn and the rest are captioned with the build that drew them ([media](docs/media/README.md)).
- Changed: the release workflows no longer build anything in this repository. A release is built privately and published here as files with checksums; `release-verify` checks the published files.
- Removed: the release note for `edb7d3ad`, replaced by the [note for `de6494fe`](docs/releases/0.5.0-de6494fe.md).
