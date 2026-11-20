# 05 Weights

What was changed in a model's weights: the transplant edits of each arm of a run, a 3D tower of the live model's layers, and, behind a toggle, how much of the weights each of the earlier 3B training hours changed. The picture below was drawn by build `edb7d3ad` and shows only the older, hour-by-hour page; it was not redrawn on `de6494fe` (see the note after it). The recording is from `185b8abd`.

## What it shows

On the current build the page opens on two things, read-only. Where a source is missing, the section says which one, in words, and never draws invented rows.

- **Transplant edits per arm** (the default). Read from the receipts of the three newest runs under the transplant runs root (`--slot-root`, or `EMBER_SLOT_RUNS_ROOT`), `<run>/receipts/*.json`. For each arm: the neurons of the slot, the weights written from the donor, the weights that really differ from the recipient, that as a share of the whole model, and whether reading the written model back matched what was written (`exact`, or `MISMATCH`). The donor and recipient themselves are not edits and are not listed. With no such receipt the section says no transplant arm has an edit receipt.
- **Inspect**: the live model drawn as a tower, one slab per layer, the embedding at the foot and the output at the top. A slab's width is the layer's share of the largest layer's bytes; its colour says whether the layer is attention, linear attention or something else. Selecting a slab opens its detail beside the tower: its tensors as bars with their shapes and types. Only the file header is read (names, shapes, types, byte ranges), never the weights. Studio picks the resident model's file in the models folder (`--models-root`), else the largest model file there, else a model folder with a `config.json` and `.safetensors` files; `EMBER_STUDIO_INSPECT_MODEL` names a file or folder instead. With no readable model the tower is not drawn.

**3B HISTORY** (a toggle in the VIEW group) brings back the older page, which is the one in the picture below: the weight-difference receipt of every earlier hour (from the receipts root, `--root`), one row per hour, newest on top.

![Weight difference per hour, and the parameters of the newest hour (build edb7d3ad)](../media/weights.png)

- The header counts the hours (`5 hours, newest on top`).
- The legend: orange is **elements changed**; dark red is **updated, not changed**.
- Each row is an hour (month-day and time in the home time zone) and a bar. The newest row also prints its count of changed elements (72,408,000 in the picture; the numbers are made up).
- Under it, **parameters of the newest hour** draws one square per parameter: changed, updated but not changed, or neither.
- The right panel shows the share changed for the selected hour.

If no receipts root is configured the page says so and gives the flag.

What was checked on `de6494fe`: the page's controls and their disabled reasons, with `ui-tree` and an offscreen render on empty folders. The transplant edit rows and the tower were not drawn for this guide, because that needs receipts and a model file; they are described from the program's manual and source.

## Controls

| Group | Control | What it does |
| --- | --- | --- |
| VIEW | 3B HISTORY | Switches to the older hour-by-hour page; press again to return |
| GROUP | BY PARAMETER / BY LAYER | Chooses whether the 3B hour rows are one per parameter or grouped by layer. Disabled, with `these group the 3B hour parameters: turn 3B history on to see them`, while 3B HISTORY is off |
| HOUR | NEWEST / OLDEST | Selects the newest or the oldest hour or arm. Disabled, with `this page has no transplant edits or weight-difference hours to pick from`, when there is nothing to pick |

BY LAYER and the HOUR buttons were not pressed on `edb7d3ad`; they were operated on `185b8abd`:

![Recording: BY LAYER, BY PARAMETER, then OLDEST and NEWEST](../media/weights.gif)

*Recording: [weights.mp4](../media/weights.mp4), build `185b8abd`.*

## Known limits of this tab

- The tower shows each layer's size and tensors from the file header. It does not show activations, attention maps or gradients; those are planned under the Inspect capability.
- The hour page reads only the weight-difference receipts that the earlier 3B hours wrote.
- In the data captured on `185b8abd` every hour's bar was full. BY LAYER was pressed and the page redrew, but the first screen looked the same as BY PARAMETER, so this guide does not describe what the layer grouping adds.
