# Ember Studio

A native desktop application for producing, investigating and understanding AI models, built around [Ember](https://github.com/wordingone/ember), a language model trained on one home computer.

Ember Studio is where Ember's training runs are started, resumed, stopped and watched, where its data library can be explored, and where models (Ember checkpoints or open-weight models) can be loaded and used.

**Status: early development.** The first screen, a live training monitor, works today; the rest is being built. Expect breaking changes.

## Planned modes

- **Monitor / Train**: live loss (per data source), throughput, learning rate and energy for a running training hour; start, resume and stop runs.
- **Library**: every dataset collected or on its way, as an explorable place; open any document; see what a training hour read.
- **Models**: load an open-weight model or an Ember checkpoint and chat, complete, or compare.
- **Evals, Weights, Experiments, Storage**: benchmark results, weight inspection, experiment records, disk and archive state.
- **ember-cli**: the Ember command line as a built-in, toggleable panel.

Every screen also has a headless JSON command so scripts and agents can use the same data.

## Build

Rust (stable). `cargo build --release` in the workspace root. Windows is the primary platform; Linux builds in CI.

## License

Source-available; see [LICENSE](LICENSE).
