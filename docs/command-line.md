# Command line and driving Studio from scripts

Every control of the window has a stable name and can be operated by a script without a mouse and without taking the keyboard focus. This page lists the commands and the roots the pages read. In examples `ember-studio` stands for the exe you run (`ember-studio.exe`). The text was checked against build `de6494fe`; the complete list of verbs, exit codes and `--act-set` names is the [command reference](interface/commands.md).

## Commands

| Command | What it does |
| --- | --- |
| `ember-studio monitor [options]` | Opens the window. Takes the roots below and `--mode SLUG` to open on a tab |
| `ember-studio monitor --headless --json` | Prints one JSON snapshot and exits; opens no window |
| `ember-studio monitor --render-png FILE [--mode SLUG] [--size WxH]` | Draws a tab offscreen to a PNG, with no window and no GPU, and prints a render receipt. Starts no window, so it does not trip the one-window rule and takes no focus. See [render options](#render-options) |
| `ember-studio --act NAME` | Operates a control of the **running** window (see below) |
| `ember-studio ui-tree [--mode SLUG] [--json] [--agent-stub SCENARIO]` | Draws a tab offscreen and prints every control's accessible name, role, value and disabled reason. Opens no window. It never reports the running window |
| `ember-studio ui-tree --live` | Reads the tab the **running** window drew last, through its own pipe, without focus or UI Automation. One line: `{"live":true,"pid":N,"tab":SLUG,"frame":N,"age_ms":N}`. Exit 1 if no Studio is running |
| `ember-studio ui-sweep [--json] [--root DIR] [--start default\|hour\|cli\|narrow\|research\|agent\|agent-streaming\|agent-done]` | Operates every drawn control offscreen, in script order and in a fresh window per control, and lists the ones that do nothing. Prints `SWEEP_PASS` and exits 0 when none is dead |
| `ember-studio windows [--pid N]` | Lists the visible top-level windows of the running Studio; exit 0 when there is exactly one |
| `ember-studio selftest-repaint [--seconds N]` | Draws frames with no input and checks the on-screen clock moves; exit 0 pass |
| `ember-studio library <subcommand>` | The Library's own command-line reader: `wings`, `shelves`, `books`, `open`, `provenance`, `acquisitions`, `census`, `search`, `status`, `bench`, `render-png`. Not exercised for this guide beyond `--help`; see [Library](tabs/library.md) |
| `ember-studio status [--job ID]` | Asks the lab about a job and reads its log, in words |
| `ember-studio press ...` / `stop ...` | Start and stop a job through the lab (see the program's `--help`; not exercised for this documentation) |

`SLUG` is one of `train`, `library`, `models`, `evals`, `weights`, `research`, `console`, `timeline`, `agent`.

Studio is a GUI program, so a shell does not wait for it. In PowerShell run a command that prints through a pipe, for example `ember-studio ui-tree | Out-String`, or `Start-Process -Wait -PassThru`, to read its output and exit code.

## Render options

`monitor --render-png` draws the real window to a file, which is how the pictures in these guides were made, and a way to check a page without opening one. Options that only a render takes:

| Option | Draws |
| --- | --- |
| `--mode SLUG` | that tab (`train`, `library`, `models`, `evals`, `weights`, `research`, `console`, `timeline`, `agent`) |
| `--size WxH`, `--scale F` | the picture size (default 1600x1000) and a scale factor |
| `--settle SECS` | waits that long after the first read, so a page that asks the lab has its answer |
| `--select KEY` | the tab with one element selected, so the right panel shows its detail. A key is `<kind>:<id>`: `pack:<name>`, `model:<slug>`, `file:<name>`, `hour:<slug>`, `pair:<TAG>`, `hyp:<id>`, `exp:<id>` and so on. A key the page does not hold is cleared |
| `--press [--script P] [--sha256 H] [--log L]` | the [Hour view](tabs/hour-view.md) with its checks and the lab's job |
| `--dock cli\|run\|sources\|energy\|lr` | the right dock open on that tab |
| `--agent-stub SCENARIO [--agent-input TEXT]` | the Agent tab on a scripted conversation: `cold`, `waking`, `awake`, `streaming`, `done`, `markdown`, `card_busy`, `card_yielded`, `card_yielding`, `card_yield_failed`, `card_held`, `error`, `asleep`, `sending` |
| `--project FILE` | Research with that project file open |
| `--band-file FILE`, `--labels PATH` | the measured noise band Evals draws, and the declared labels the Train learning curve reads |
| `--train-dream`, `--series-max N`, `--library-grow N`, `--compare-pair`, `--compare-layer`, `--compare-a` | render-only choices: the Train DREAM badge lit, the number of points drawn, a Library that has grown by N packs, and which pair, layer and model the Models compare frame holds. Listed in the program's help; not used for these guides |
| `--train-history`, `--dock-history`, `--history`, `--lineage`, `--compare` | the old 3B views, the dock's history rows, Evals history, the Models lineage and the compare frame |

Exit codes: 0 rendered, 3 bad arguments, 4 render failed. A render with no root flags looks for the usual folders on the machine it runs on, so pass the roots when a picture must not depend on them. A page reads its sources once in a render and says so (`read once`).

## Operate the running window: `--act`

```
ember-studio --act mode.evals
ember-studio --act ribbon.evals.history --act ribbon.evals.pair_oldest
```

A second launch hands the name to the running window, which receives the same click a mouse would send, inside its own event loop. No UI Automation call and no operating-system input is used, so the window never takes the keyboard focus. Several `--act` flags run in order. With no Studio running it exits with code 4 and opens nothing.

Names are the ones `ui-tree` prints. The shell and the tab buttons:

| Name | Control |
| --- | --- |
| `mode.agent` `mode.train` `mode.library` `mode.models` `mode.evals` `mode.weights` `mode.research` `mode.console` `mode.timeline` | the nine mode tabs |
| `menu.file` `menu.view` `menu.help`, `menu.help.keys`, `menu.help.about` | menus and the two Help items |
| `status.local` | the LOCAL · NO CLOUD chip |
| `panel.cli.toggle`, `ribbon.window.agent_dock` | the ember-cli panel and the agent dock |
| `train.method.full` `train.method.lora` `train.method.qlora` | Train: the finetune method (the dormant pretrain tile cannot be chosen) |
| `ribbon.train.history` `ribbon.raw` `ribbon.mixed_ema` `ribbon.sources` `ribbon.dock` `ribbon.hour` `rail.loss` `rail.curve` `rail.tok_s` `rail.power` `dock.run` `dock.sources` `dock.energy` `dock.lr` | Train |
| `ribbon.library.room` `ribbon.library.rescan` `ribbon.library.sort_newest` `ribbon.library.sort_size` | Library |
| `ribbon.models.lineage` `ribbon.models.compare` | Models |
| `ribbon.evals.history` `ribbon.evals.pair_newest` `ribbon.evals.pair_oldest` `ribbon.evals.arm_fresh` `ribbon.evals.arm_intake` `ribbon.evals.sort_weakest` | Evals |
| `ribbon.weights.history` `ribbon.weights.group_parameter` `ribbon.weights.group_layer` `ribbon.weights.newest` `ribbon.weights.oldest` | Weights |
| `net3d.exp.<id>` `net3d.layer.all` `net3d.layer.<n>` `net3d.donor.view_top` `paper.toggle` | Research |
| `ribbon.timeline.range_hour` `ribbon.timeline.range_day` `ribbon.timeline.range_all` `ribbon.timeline.source_all` `ribbon.timeline.source_press` `ribbon.timeline.source_lab` | Timeline |
| `ribbon.console.follow` `ribbon.console.errors_only` `ribbon.console.job_state` | Console |

A disabled control has a read-out named like it with `.reason` added; an on-state toggle has one with `.on` added.

Filling a text box uses `--act-set NAME VALUE` and `--act-clear NAME`. The names it accepts are `agent.input`, `agent.folder`, `agent.dock.input`, `agent.newcmd.*`, `press.script`, `press.sha256`, `press.log`, `train.method` and `research.project.*`; any other name is refused, nothing is applied, and the exit code is 5 (`ACT_SET_REFUSED`). Then `--act agent.send` sends the Agent tab's turn. The answer is read from `ui-tree --live`.

Never use UI Automation's Invoke on the window: Windows activates the target window for it, which takes the keyboard focus whatever the application does. `--act` exists to avoid exactly that.

## One window

`monitor` while a window exists opens nothing: it passes `--script`, `--sha256`, `--log` and `--press` to the open window, prints `STUDIO_ALREADY_RUNNING pid=<n>` and exits 0. A setting only a new window can take (for example `--lab-pipe`) is reported as ignored.

## Roots the pages read

A flag beats its environment variable. A root that is set but missing is reported as missing, with its path.

| Flag | Environment variable | Used by |
| --- | --- | --- |
| `--data-root DIR` | `EMBER_LANE_ROOT` | Library: reads `<DIR>/packed/*` |
| `--models-root DIR` | `EMBER_STUDIO_MODELS_ROOT` | Models: the folder of model files |
| `--learn-root DIR` | `EMBER_STUDIO_LEARN_ROOT` | Research: a folder per learn run |
| `--slot-root DIR` | `EMBER_SLOT_RUNS_ROOT` | Evals: the transplant runs root (a folder per press) |
| `--delta-root DIR` | `EMBER_DELTA_MAP_ROOT` | Models compare: delta maps |
| `--nll-root DIR` | `EMBER_EPISODE_NLL_ROOT` | Evals history and the Train learning curve |
| `--root DIR` | `EMBER_LIVE_RECEIPTS_ROOT` | Train, Weights, Models lineage: the receipts of earlier hours |
| `--press-receipts FILE` | `EMBER_STUDIO_PRESS_RECEIPTS` | Console, Timeline (default `%LOCALAPPDATA%\ember-studio\press-receipts.jsonl`) |
| `--lab-pipe NAME` | `EMBER_STUDIO_LAB_PIPE` | every call to the lab (default `studio`) |
| `--home-tz FILE` | `EMBER_HOME_TZ` | the time zone every drawn clock reads; with none readable, UTC |

Other settings: `--cli-exe`, `--cli-arg`, `--cli-cwd`, `--cli-env` (the ember-cli panel's program), `--x5-receipt`, `--floor-gib`, `--env`, `--cwd`, `--bash` (the Hour view's request). `--help` prints them all.

## Exit codes

`monitor` 0 ok, 2 no source (headless), 3 bad arguments, 4 render failed. `ui-tree` 0 ok, 3 bad arguments. `status` 0 read, 2 nothing to read. `press` 0 started, 2 refused, 3 bad arguments, 4 failed. `stop` 0 ended, 2 refused, 4 failed, 6 not confirmed, 7 not ended. `--act` with no running window: 4 (`STUDIO_NOT_RUNNING`). `--act-set` with a name it does not accept: 5. `ui-tree --live` with no Studio running: 1. `ui-sweep` 0 no dead control. `windows` 0 exactly one visible window. `selftest-repaint` 0 pass, 1 fail.

The window and every other Studio process pin themselves to two logical CPUs at below-normal priority; `--cpu-mask` or `EMBER_STUDIO_CPU_MASK` changes the pin (see [window](window.md#cpu-and-priority)).
