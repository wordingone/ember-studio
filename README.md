# Ember Studio

A native desktop research environment for producing, investigating and understanding AI models, built around [Ember](https://github.com/wordingone/ember). Studio draws models, data and experiments as things you look at and move around in, and it talks to a resident daemon, **ember-lab**, that owns every training run and model server.

![The Library tab: every data pack drawn as a book on a shelf in a 3D room](docs/media/library-room.png)

*The Library tab in its 3D room view: the data packs drawn as books on shelves, with a footer that counts books, shelves, local, Hugging Face only and arriving. More screenshots and recordings are in the [tab guides](docs/tabs/).*

**Status: early development (v0.5.0).** Studio runs on Windows today. Linux and macOS builds do not exist yet; [what blocks them](docs/platforms.md) is written down. Several parts of the program are read-only viewers while the lab learns new job kinds; each guide says exactly what works. Expect breaking changes.

## Download

| Platform | Build | Status |
| --- | --- | --- |
| Windows 10/11, x64 | `ember-studio-0.5.0-185b8abd-windows-x64.zip` from the [Releases page](https://github.com/wordingone/ember-studio/releases) | available once the release is published |
| Linux | none | not built yet; see [platforms](docs/platforms.md) |
| macOS | none | not built yet; see [platforms](docs/platforms.md) |

Verify the download against `SHA256SUMS` on the release page before you run it. Step by step instructions: [docs/install.md](docs/install.md).

## Quick start (Windows)

1. Unzip, then run `ember-studio-185b8abd.exe` (no installer, no console window).
2. The window opens on the tab you used last. Press `Ctrl+9` for the Agent tab or `Ctrl+1` to `Ctrl+8` for the others.
3. Studio reads files on your machine and asks ember-lab questions over a local pipe. With no lab running, the pages that need it say so in words; nothing breaks.
4. Point a page at your data with a flag, for example `ember-studio-185b8abd.exe monitor --models-root <folder of models> --data-root <folder of data packs>`. The full list of roots is in [docs/command-line.md](docs/command-line.md).

Start with [Getting started](docs/getting-started.md).

## What Studio is for

Studio is built around five capabilities. Where each stands today is in [Getting started](docs/getting-started.md#the-five-capabilities-and-what-works-today).

- **Construct**: architectures, datasets, training pipelines.
- **Experiment**: configure, queue, run and compare experiments.
- **Inspect**: weights, activations, representations, how a checkpoint differs from its parent.
- **Investigate capability**: score what a model can do, find weaknesses, test an intervention.
- **Automate research**: agents that design and run experiments, with a human approving.

## The nine tabs

| Tab | What it is | Guide |
| --- | --- | --- |
| 00 Agent | A chat with the resident model that reads and edits files in a working folder you choose, with approvals | [agent](docs/tabs/agent.md) |
| 01 Train | The job the lab is running now; start, watch and stop an hour; charts of past hours | [train](docs/tabs/train.md) |
| 02 Library | The data library as a 3D room or a size-sorted list | [library](docs/tabs/library.md) |
| 03 Models | The models in play, the checkpoint lineage, and a side by side compare | [models](docs/tabs/models.md) |
| 04 Evals | Transplant pairs against a significance bar, and the old held-out score per hour | [evals](docs/tabs/evals.md) |
| 05 Weights | How much of the weights each hour changed | [weights](docs/tabs/weights.md) |
| 06 Research | A research project file, 3D donor and recipient networks, live experiments, a paper pane | [research](docs/tabs/research.md) |
| 07 Console | The lab's job events and the job log | [console](docs/tabs/console.md) |
| 08 Timeline | Press receipts and lab events in time order | [timeline](docs/tabs/timeline.md) |

## Documentation

- [Install](docs/install.md) and [platforms](docs/platforms.md)
- [Getting started](docs/getting-started.md)
- [The window: menus, ribbon, docks, keys](docs/window.md)
- [How Studio talks to ember-lab](docs/lab.md)
- [Command line and driving Studio from scripts](docs/command-line.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Known limits](docs/known-limits.md)
- [Screen recordings](docs/media/README.md)

## Contributing

This repository holds documentation, examples, manifests and released builds. It does not hold the program's source. Issues are welcome; a pull request here can change documents and examples, not program behaviour. [Known limits](docs/known-limits.md) lists what is missing and is a good place to start an issue.

## License

See [LICENSE](LICENSE). It covers what is in this repository. Released program files carry their own terms.
