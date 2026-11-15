# 01 Train

The job the lab is running now, as three cards; the right dock with its four tabs; and the way into the [Hour view](hour-view.md) for starting, watching and stopping an hour. The pictures were drawn by build `edb7d3ad`; see [how the pictures were made](#how-the-pictures-were-made).

## What it shows

With a job running, the page shows it as three cards: how long it has run, which arm it is on, and the GPU card.

![Train with a learn job running](../media/train-job.png)

- A badge (LEARN, or the hour kind) and RUNNING with a spinner, then the job's name (in the picture, `demo-pair`).
- **RAN FOR**: a clock and an elapsed time.
- **ARM**: the arm being scored, its data source (`bench-main` here), its chunk, tokens per second once the log has them, and a bar of arms done ("3 of 6 arms done").
- **CARD**: power draw against the card's limit, and how busy the GPU is.
- The **menu bar** chip at the top right names what holds the card (`CARD: LEARN demo-pair`).

The **right dock** has four tabs: RUN, SOURCES, ENERGY and LR. RUN repeats the job's badge, clock and arm bar in a narrow column. SOURCES lists the tag, arm and bench the job is reading.

![Train with the right dock on SOURCES](../media/train-dock-sources.png)

ENERGY and LR were not drawn for this guide.

With no job and nothing from the lab, the page says `lab not answering` (the lab is not part of the preview release; see [Known limits](../known-limits.md)). The old 3B hour charts (loss by source, the learning curve, throughput, power) are still there behind **3B HISTORY**; they read the receipts of earlier hours from `--root`. They were checked on build `185b8abd` and not redrawn for this guide:

![Train with 3B HISTORY on: four tiles and four charts](../media/train-charts.png)

## Controls

| Group | Control | What it does |
| --- | --- | --- |
| RUN | HOUR | Opens the [Hour view](hour-view.md); press again to close it |
| RUN | STOP | Asks the lab to stop the followed job. Disabled, with the reason `no running job found: nothing to stop`, when nothing is running |
| SOURCE | FOLLOW LATEST | On: follow the newest source. Off: stay on the one being read |
| LOSS VIEW | SOURCES / RAW / MIXED EMA | Which loss lines the loss chart draws: per source, the raw mixed loss, or its moving average |
| VIEW | DOCK | Shows or hides the right dock |
| VIEW | EMBER-CLI | Shows or hides the ember-cli panel |
| VIEW | FIT | Puts every chart back to all its data |
| VIEW | 3B HISTORY | Switches between the running job's cards and the charts of the earlier 3B hours |
| EXPORT | JSON | Copies the current snapshot, as JSON, to the clipboard |
| WINDOW | three icons | Agent drawer, ember-cli panel and the dock; a dock history toggle draws the old 3B hour rows in the dock's four tabs instead of the job the lab holds |

The **left rail** (HOUR, LOSS, CURVE, TOK/S, POWER) takes one chart across the whole canvas; press the same button again to give the four back. HOUR is the Hour view; the other four are the charts.

Operated for this guide, on build `edb7d3ad` offscreen: the page with a running job, the dock's RUN and SOURCES tabs, and the Hour view. Described from the control list, not pressed: FOLLOW LATEST, FIT, JSON and STOP, and the dock's ENERGY and LR tabs. A recording of the earlier build is in [media](../media/README.md).

## How the pictures were made

The pictures on this page, [Hour view](hour-view.md), [Agent](agent.md), [Library](library.md) and [Research](research.md) are not screenshots of anyone's session. They were drawn by `ember-studio monitor --render-png` (see [command line](../command-line.md)), which draws the real window offscreen: no window opens, no GPU is used and no focus is taken. The data is made up: a folder of small fake packs and models, and a stand-in lab that answers the lab's pipe with one scripted job named `demo-pair`. The stand-in lab is not ember-lab; it only lets the page draw a running job.

## A typical task: watch a running job

1. Open Train. The cards follow the job the lab reports.
2. Press RAW or MIXED EMA to change the loss lines (3B HISTORY on), or open the dock's SOURCES tab to see what the job reads.
3. Open [Console](console.md) for the job's events and log tail, or [Timeline](timeline.md) for every receipt in time order.
4. To start or stop an hour, use the [Hour view](hour-view.md).
