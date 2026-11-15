# Known limits

What does not work, is not built, or was not checked in build `edb7d3ad` (v0.5.0 preview; the recordings, the 3B history pictures and the Library list view are from `185b8abd`). Nothing here is described as a feature anywhere else in these docs.

## Not in this release

- **No lab daemon, and Studio needs it.** This is a preview of Studio only. The lab release is pending until its folders are configurable; no date is promised. Starting or stopping a job, live job state and the Agent tab's model all need the lab and do not work without it. ember-lab is built from the same commit but is not released: it still contains fixed paths to the author's machine (its card lock folder, model server and model locations), so it would not run on another computer. Studio says plainly when the lab is absent. Releasing the lab needs those paths turned into settings first.
- **No Linux and no macOS download.** A Linux build compiles and draws in WSL but its tests do not build, so it is not released; there is no macOS build. See [platforms](platforms.md).
- **Linux Studio needs a Linux ember-lab.** Blocker: a Linux Studio can draw its tabs, but everything that asks the lab has nothing to talk to, because the lab's Windows-only parts (its card lock, its fixed paths and its named pipe) exist only for Windows. Cure: port those parts of the lab to Linux (a Unix socket in place of the pipe, a portable card lock, paths as settings). That work is queued in the lab's task list after the folder settings, and a Linux Studio release follows it. No date is promised.
- **The build is not code-signed.** Windows SmartScreen may warn.
- **Terms for the released program** are separate from this repository's licence; they have not been published yet. Read [LICENSE](../LICENSE) for what it covers.

## Not built yet (the five capabilities)

- **Construct**: no architecture editor, no dataset mixtures, no pipeline editor.
- **Experiment**: no saved experiment form with typed hyperparameters, no queue, and no compare of two runs' hyperparameters. Starting a job is the Hour view's form.
- **Inspect**: no tensors, activations, attention maps or gradients. Weights shows counts of changed elements only.
- **Investigate capability**: Evals reads results; it cannot start an evaluation, and there is no hypothesis record linked to a test.
- **Automate research**: the Agent tab chats and edits files under approvals; there is no proposal inbox where an agent files an experiment for you to approve.

## Built but not exercised while writing these docs

- Starting and stopping a training hour from the [Hour view](tabs/hour-view.md). Its picture is a render against a stand-in lab that refuses a second hour; START and STOP were never pressed.
- The Research project controls (NEW, OPEN, SAVE, ADD EXPERIMENT, ADD HYPOTHESIS, ADD MODEL), and the paper pane's `source` and `recompile`. The Research picture's project was opened with the render verb, not the buttons.
- Picking models into the Models compare frames, and the compare control on an Evals pair.
- The Library room's HUD button and mouse navigation of the 3D room; the Train FOLLOW LATEST, FIT and JSON buttons; the Train dock's ENERGY and LR tabs.
- The Agent tab's approvals, session list and `--act-set` route. The Agent tab pictures are drawn on a scripted conversation, not a live model, and there is no recording of it, so that no real session is published. The yield states (`YIELDING`, `YIELDED`, `yield failed`) are drawn from scripted scenarios; a real yield to a job was not run for this guide.
- Console's FOLLOW, ERRORS ONLY and JOB STATE; Timeline's 1H, 24H, PRESS and LAB; Evals' HISTORY and the pair compare control; Weights' BY LAYER and HOUR buttons. They were operated on `185b8abd`, and only drawn in their default state on `edb7d3ad`.
- Studio on a machine without an NVIDIA GPU.

## Behaviour worth knowing

- Studio pins itself to logical CPUs 30 and 31 at below-normal priority when the machine has them. On smaller machines the pin is skipped.
- The Weights page prints counts only. In the captured data every bar is full, so the layer grouping looked identical to the parameter grouping.
- Several pages show the author's research data (donors, recipients, transplant pairs, earlier training hours). They are drawn from whatever folders you configure; on a machine without those folders the pages say which flag to give.
