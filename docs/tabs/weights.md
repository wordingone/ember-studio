# 05 Weights

How much of a model's weights each training hour changed. Checked on build `185b8abd`.

## What it shows

The page reads the weight-difference receipt of every hour (from the receipts root, `--root`) and draws one row per hour, newest on top.

![Weight difference per hour](../media/weights.png)

- The header counts the hours, for example "57 hours, newest on top".
- The legend: orange is **elements changed**; dark red is **updated, not changed**.
- Each row is an hour (month-day and time) and a bar. The newest row also prints its count of changed elements (71,844,480 in the captured data).
- The right panel shows the share changed for the selected hour (100.0% in the captured data).

If no receipts root is configured the page says so and gives the flag.

## Controls

| Group | Control | What it does |
| --- | --- | --- |
| GROUP | BY PARAMETER / BY LAYER | Chooses whether the rows are one per parameter or grouped by layer |
| HOUR | NEWEST / OLDEST | Selects the newest or the oldest hour |

![Recording: BY LAYER, BY PARAMETER, then OLDEST and NEWEST](../media/weights.gif)

*Recording: [weights.mp4](../media/weights.mp4).*

## Known limits of this tab

- The page shows counts only. It does not show tensors, per-layer histograms or gradients; those are planned under the Inspect capability.
- In the captured data every hour's bar is full. BY LAYER was pressed and the page redrew, but the first screen looked the same as BY PARAMETER, so this guide does not describe what the layer grouping adds.
