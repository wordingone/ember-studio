# Getting started

Everything here was checked against the Windows build `185b8abd` (Ember Studio v0.5.0) running on Windows 11. Where something is not working yet it is in [Known limits](known-limits.md), never described here as a feature.

## 1. Install and open

Follow [install](install.md), then run `ember-studio-185b8abd.exe`. A single window titled "Ember Studio" opens. Studio is a Windows GUI program: no console opens with it, and closing the terminal you started it from does not close it.

Only one Studio window can exist on a machine. Starting a second one opens nothing; it hands its arguments to the first window, prints `STUDIO_ALREADY_RUNNING pid=<n>` and exits. See [command line](command-line.md).

## 2. Read the window

![The Train tab with its ribbon, left rail and right dock](media/train-charts.png)

Top to bottom:

- **Menu bar**: FILE, VIEW, HELP, then two chips on the right. The first names what is holding the GPU card right now (in the screenshot, a learn job); the second reads LOCAL · NO CLOUD and opens a sentence saying what Studio reads and talks to ([window](window.md)).
- **Mode tabs**: `00 AGENT` through `08 TIMELINE`. `Ctrl+9` opens Agent and `Ctrl+1` to `Ctrl+8` open the others.
- **Ribbon**: the buttons of the current tab, in labelled groups. A disabled button carries the reason it is off (`ui-tree` prints it; see [command line](command-line.md)).
- **Page**: the tab itself. Most pages re-read their sources every 4 seconds while the tab is open and say when they last read.
- **Agent drawer**: a collapsed strip at the foot of every page; SHOW opens the agent beside the page you are on.

[The window](window.md) lists every shell control.

## 3. Tell Studio where your files are

Studio is a client of two things: files on your disk and a running ember-lab. A page whose source is not configured says which flag to give, in words, for example `no models folder is configured: pass --models-root DIR`. Start Studio with the roots you have:

```
ember-studio-185b8abd.exe monitor --models-root <models folder> --data-root <data packs folder> --learn-root <learn runs folder>
```

The full list of roots, and what each tab reads, is in [command line](command-line.md#roots-the-pages-read).

## 4. The five capabilities and what works today

Studio is organised around five things a research environment must let you do. This is the honest state of each in this build.

| Capability | What you can do today | What you cannot do yet |
| --- | --- | --- |
| Construct | See the models on disk, grouped by role ([models](tabs/models.md)). The Research tab has project-file buttons (NEW, OPEN, SAVE, ADD EXPERIMENT, ADD HYPOTHESIS, ADD MODEL) that this guide did not exercise ([research](tabs/research.md)) | Draw or edit an architecture, compose datasets into a mixture, edit a training pipeline |
| Experiment | Start, watch and stop a governed training hour through the lab ([train](tabs/train.md)); read finished and running jobs ([console](tabs/console.md), [timeline](tabs/timeline.md)) | A saved experiment form with typed hyperparameters, a queue, a compare view of two runs' hyperparameters |
| Inspect | A two-model compare frame on Models ([models](tabs/models.md#compare)); how much of the weights an hour changed ([weights](tabs/weights.md)); donor and recipient networks drawn in 3D with their layers ([research](tabs/research.md)) | Per-layer tensors, activations, attention maps and gradients on a prompt |
| Investigate capability | Read transplant pairs scored against a 3 SE bar, with donor and recipient scores ([evals](tabs/evals.md)) | Start an evaluation from Studio, write a hypothesis against a weakness and link the test |
| Automate research | Chat with the resident model, which reads and edits files in a working folder you choose, under approvals ([agent](tabs/agent.md)) | A proposal inbox where an agent files an experiment for you to approve |

## 5. A first ten minutes

1. Open **02 Library**. Press ROOM to switch between the 3D room and the size-sorted list ([library](tabs/library.md)).
2. Open **03 Models**. Press 3B LINEAGE and back; press COMPARE to see the two-model frame ([models](tabs/models.md)).
3. Open **04 Evals**. Each dot is a donor and recipient pair; the dashed line is the 3 SE bar ([evals](tabs/evals.md)).
4. Open **06 Research**. Switch the experiment with the buttons above the two networks, and filter by layer ([research](tabs/research.md)).
5. Open **01 Train** and press 3B HISTORY to see the charts of the earlier training hours ([train](tabs/train.md)).

Short screen recordings of each of these are in [media](media/README.md).

## 6. Drive Studio from a script

Every control has a stable name and can be operated without a mouse and without taking the keyboard focus: `ember-studio-185b8abd.exe --act mode.evals` switches the running window to Evals. See [command line](command-line.md).
