# Known limits

What does not work, is not built, or was not checked in build `de6494fe` (v0.5.0 preview). The text of the guides was checked against that build's source and, where it says so, the built program run offscreen; the pictures are from three builds (`de6494fe`, `edb7d3ad`, `185b8abd`), and each guide says which beside the picture ([the list](media/README.md)). Nothing here is described as a feature anywhere else in these docs.

## Not in this release

- **No release has been published.** Studio and ember-lab are built from the same source, but neither has a download yet, and no date is promised. Studio needs a lab to start, watch or stop a job, to show live job state and to run the Agent tab's resident model, and it says plainly when the lab is absent. The lab no longer has folders fixed to one machine: its card lock, press records, tools, resident model files, mail, logs and the custody drive are settings (`ember-lab.toml` or environment variables; `ember-lab paths` prints them), described in [lab](lab.md). Whether the lab runs correctly on a machine other than the one it was developed on was not tested, and the models, card and training data it expects are yours to provide.
- **No Linux and no macOS build.** A Linux build compiled and drew in WSL on an earlier build (`185b8abd`) but its tests did not build; this was not re-measured on the current source. There is no macOS build. See [platforms](platforms.md).
- **Linux Studio needs a Linux ember-lab.** Blocker: a Linux Studio can draw its tabs, but everything that asks the lab has nothing to talk to, because the lab's Windows-only parts (its card lock, job control and its named pipe) exist only for Windows. Cure: port those parts of the lab to Linux (a Unix socket in place of the pipe, a portable card lock). The folders are already settings. A Linux Studio release follows that work. No date is promised.
- **The build is not code-signed.** Windows SmartScreen may warn.
- **Terms for the released program** are separate from this repository's licence; they have not been published yet. Read [LICENSE](../LICENSE) for what it covers.

## Not built yet (the five capabilities)

- **Construct**: no architecture editor, no dataset mixtures, no pipeline editor.
- **Experiment**: no saved experiment form with typed hyperparameters, no queue, and no compare of two runs' hyperparameters. Starting a job is the Hour view's form.
- **Inspect**: no activations, attention maps or gradients. Weights shows the transplant edits of each arm and, from the file header, the layers and tensors of the live model; it reads no weight values.
- **Investigate capability**: Evals reads results; it cannot start an evaluation, and there is no hypothesis record linked to a test.
- **Automate research**: the Agent tab chats and edits files under approvals; there is no proposal inbox where an agent files an experiment for you to approve. `/compact` is not a Studio command yet (compaction happens by itself).

## Built but not exercised while writing these docs

- Starting and stopping a training hour from the [Hour view](tabs/hour-view.md). Its picture is a render against a stand-in lab that refuses a second hour; START and STOP were never pressed.
- The Research project controls (NEW, OPEN, SAVE, ADD EXPERIMENT, ADD HYPOTHESIS, ADD MODEL), and the paper pane's `source` and `recompile`. The Research picture's project was opened with the render verb, not the buttons.
- Picking models into the Models compare frames, and the compare control on an Evals pair.
- The Library room's HUD button and mouse navigation of the 3D room; the Train FOLLOW LATEST, FIT and JSON buttons; the Train dock's ENERGY and LR tabs.
- The Agent tab against a live model: approvals, the session list, compaction, the state line's two numbers, the cut notes, the external provider route (a model named in a provider config file) and the tab being drawn disabled when the lab cannot serve it. These were read from the source and its tests, and the stub scenarios were drawn offscreen; no model was started for this guide. The Agent tab pictures are drawn on a scripted conversation, and there is no recording of it, so that no real session is published. The yield states (`YIELDING`, `YIELDED`, `yield failed`) are drawn from scripted scenarios; a real yield to a job was not run for this guide.
- Console's FOLLOW, ERRORS ONLY and JOB STATE; Timeline's 1H, 24H, PRESS and LAB; Evals' HISTORY and the pair compare control; Weights' BY LAYER and HOUR buttons. They were operated on `185b8abd`, and only drawn in their default state on later builds.
- The Weights tab's transplant-edit rows and layer tower, the Models compare delta band and the Research press chips and live-experiment cards: described from the source and the program's manual, not drawn, because they need run folders, a model file or a lab. The Train mode strip was drawn with no lab and no GPU reading.
- The disk-backed `ember-studio library` subcommands (`open`, `provenance` and the rest) beyond `--help`.
- Studio on a machine without an NVIDIA GPU.

## Behaviour worth knowing

- Studio pins itself to logical CPUs 30 and 31 at below-normal priority. A machine that cannot grant that gets no pin and Studio goes on; `--cpu-mask` or `EMBER_STUDIO_CPU_MASK` changes it.
- In the 3B history data captured on `185b8abd` every bar was full, so the layer grouping looked identical to the parameter grouping.
- Pretraining is shown dormant on the Train tab and cannot be chosen; the lab refuses it too.
- Several pages are built around the author's research data (donors, recipients, transplant pairs, earlier training hours). They draw whatever is in the folders you configure; with a flag or variable missing, the page says which. Without a flag, a page looks in a conventional place on a drive of the machine it runs on (for example a folder named `models`), so a render on a machine that has such folders can show their contents; pass the roots explicitly when that matters.
