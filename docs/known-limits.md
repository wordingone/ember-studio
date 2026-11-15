# Known limits

What does not work, is not built, or was not checked in build `185b8abd` (v0.5.0). Nothing here is described as a feature anywhere else in these docs.

## Not in this release

- **No lab daemon.** ember-lab is built from the same commit but is not released: it still contains fixed paths to the author's machine (its card lock folder, model server and model locations), so it would not run on another computer. Studio therefore shows what it can read from files and says plainly when the lab is absent. Releasing the lab needs those paths turned into settings first.
- **No Linux and no macOS build.** See [platforms](platforms.md).
- **The build is not code-signed.** Windows SmartScreen may warn.
- **Terms for the released program** are separate from this repository's licence; they have not been published yet. Read [LICENSE](../LICENSE) for what it covers.

## Not built yet (the five capabilities)

- **Construct**: no architecture editor, no dataset mixtures, no pipeline editor.
- **Experiment**: no saved experiment form with typed hyperparameters, no queue, and no compare of two runs' hyperparameters. Starting a job is the Hour view's form.
- **Inspect**: no tensors, activations, attention maps or gradients. Weights shows counts of changed elements only.
- **Investigate capability**: Evals reads results; it cannot start an evaluation, and there is no hypothesis record linked to a test.
- **Automate research**: the Agent tab chats and edits files under approvals; there is no proposal inbox where an agent files an experiment for you to approve.

## Built but not exercised while writing these docs

- Starting and stopping a training hour from the Hour view. A real job was running, so START and STOP were never pressed.
- The Research project controls (NEW, OPEN, SAVE, ADD EXPERIMENT, ADD HYPOTHESIS, ADD MODEL), and the paper pane's `source` and `recompile`.
- Picking models into the Models compare frames, and the compare control on an Evals pair.
- The Library room's HUD button and mouse navigation of the 3D room; the Train FOLLOW LATEST, FIT and JSON buttons; the Train dock's SOURCES, ENERGY and LR tabs at full width.
- The Agent tab's approvals, session list and `--act-set` route. The Agent tab screenshots are drawn on a scripted conversation, not a live model, and there is no recording of it, so that no real session is published.
- Studio on a machine without an NVIDIA GPU.

## Behaviour worth knowing

- Studio pins itself to logical CPUs 30 and 31 at below-normal priority when the machine has them. On smaller machines the pin is skipped.
- The Weights page prints counts only. In the captured data every bar is full, so the layer grouping looked identical to the parameter grouping.
- Several pages show the author's research data (donors, recipients, transplant pairs, earlier training hours). They are drawn from whatever folders you configure; on a machine without those folders the pages say which flag to give.
