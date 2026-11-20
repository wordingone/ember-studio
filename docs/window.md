# The window: menus, ribbon, docks, keys

The parts of the window that are the same on every tab. The text was checked against build `de6494fe` (source and `ui-tree`); the pictures are from `185b8abd`.

## Menu bar

![The Help menu open, listing Keyboard and About Ember Studio](media/menu-help.png)

- **FILE**, **VIEW**, **HELP** open lists; Esc or a click elsewhere closes one.
- HELP has **Keyboard** and **About Ember Studio**. Each leaves a one-line note in the menu bar (an × dismisses it). Keyboard lists the keys below; About says the version (v0.5.0 in this build) and that Studio "reads files on this machine and talks to ember-lab over a local pipe" and starts and stops nothing itself. FILE also holds Create new research project, the Hour view and Copy snapshot; VIEW holds the run dock, the ember-cli panel, Fit, and Developer mode (off by default; while on, Studio re-applies a `dev-overlay.json` of colours, spacing and label text to the open window as it is saved).
- The two chips on the right:
  - on Train, the **run chip** reads `No job` or names the lab's running job (for example `Card: learn <name>`); on every other tab the bar shows the tab's own name instead;
  - **LOCAL · NO CLOUD** opens a sentence: Studio reads files on this machine and talks to ember-lab over a local named pipe, opens no network connection and sends nothing off the PC; the ember-cli panel runs a program you gave it and that program is not Studio.

![The LOCAL NO CLOUD chip open](media/status-local.png)

## Mode tabs

A tab the lab cannot serve is drawn disabled, with the reason as hover text, and a click does nothing: Train needs the lab's start, check and job-list verbs; Console and Timeline need its job-event verbs; Agent needs its agent-turn verbs. Library, Models, Evals and Weights never need the lab, and Research needs it only for job state. A lab with no `capabilities` verb leaves every tab on, and so does an offscreen render. This is from the source and its unit test; it was not run in a live window for this guide.

`00 AGENT`, `01 TRAIN`, `02 LIBRARY`, `03 MODELS`, `04 EVALS`, `05 WEIGHTS`, `06 RESEARCH`, `07 CONSOLE`, `08 TIMELINE`. Choosing one shows that page at once. The ribbon below the tabs changes with the tab; the groups it shows are listed on each [tab page](tabs/).

## Ribbon

Buttons come in groups with a small caption under each group (RUN, SOURCE, LOSS VIEW, VIEW, EXPORT, WINDOW on Train). Some buttons are toggles and show an orange outline while on. A disabled button states its reason. The **WINDOW** group at the right of every ribbon has icon buttons: one shows or hides the agent dock, one shows or hides the ember-cli panel, and Train has a third for the right dock.

## Keys

`Ctrl+1` to `Ctrl+8` pick a mode (Train to Timeline), `Ctrl+9` picks the Agent tab, `` Ctrl+` `` (control and the backtick key) shows or hides the ember-cli panel, `Ctrl+J` shows or hides the agent dock on any tab but Agent, Tab moves between controls, Enter or Space presses the focused one, Esc closes a list.

## Right dock (Train)

A tab strip on the right edge of Train: RUN, SOURCES, ENERGY, LR. RUN shows the lab job's clock, the arm being scored and the card (`lab not answering` with no lab); SOURCES, ENERGY and LR are the other three tabs of the dock (not captured in the screenshots here). In a narrow window the strip is vertical and only labels show; at about 1400 pixels wide the dock opens as a panel.

![The right dock showing the RUN tab](media/train-dock.png)

## Agent dock

The agent docked at the foot of every tab but Agent: the same session as the Agent tab, with its state, mode chip, transcript and message box. HIDE (or `Ctrl+J`) puts it away and leaves a thin strip with SHOW. The default is shown, one third of the window's height; the height you drag it to is remembered. In a window too short for it, the dock is one line that says to close the ember-cli panel or make the window taller.

## ember-cli panel

A terminal panel for one program you name at start (`--cli-exe`). Without one it says `no program configured: give --cli-exe PATH or set EMBER_STUDIO_CLI_EXE` and starts nothing. It is a convenience; starting, watching and stopping a job is done with the Train tab's own controls.

## One window, always

There is no way to open a second Studio window. A second launch sends its arguments to the first and exits with `STUDIO_ALREADY_RUNNING pid=<n>`. This is on purpose: one window means one owner of the screen and no two windows fighting over the same lab.

## CPU and priority

Studio is deliberately light. By default every Studio process pins itself to logical CPUs 30 and 31 at below-normal priority, so it never competes with a training job for cores. A mask the machine cannot grant is not an error: the pin is recorded as not applied and Studio goes on. `--cpu-mask <mask>` or `EMBER_STUDIO_CPU_MASK` overrides it (a hex mask, a range such as `30-31`, a list such as `30,31`, or `none` to leave the CPUs alone and lower only the priority).
