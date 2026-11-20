# Roadmap

Plans, not features. Nothing here is described as working anywhere else in these docs until a release says so; what works today is in [the five capabilities](docs/capabilities.md) and what does not is in [known limits](docs/known-limits.md). No dates are promised.

## Near

- A first release: Studio and ember-lab for Windows, published as files with checksums, after the terms for released programs are published and the program has been operated from the released files against these docs.
- A model picker in the Agent tab: list the models the lab and your provider config know, show which is loaded, switch through the lab, show load progress and the reason a load failed.
- A hardware scan: read the machine's video memory, RAM, cores and free disk at run time and say which models fit and at what context, instead of leaving the choice to trial and error.
- Faster model serving through Studio: measured baselines for load, prompt reading and generation, and the settings that improve them, published with their numbers.

## Later

- A Linux build, which needs a Linux ember-lab first ([platforms](docs/platforms.md)).
- The capabilities listed as "cannot yet" in [the five capabilities](docs/capabilities.md): an experiment form with typed hyperparameters and a queue, activations and attention maps on a prompt, starting an evaluation from Studio, and a proposal inbox for an agent's experiments.
- Wider support for provider config files.
