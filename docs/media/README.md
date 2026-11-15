# Screen recordings

Each recording is a sequence of frames of the one running Studio window, captured with the Windows PrintWindow call about five times a second while the window was driven with `ember-studio --act` (no mouse, no keys, no focus taken), then encoded to H.264 (mp4) and to a small GIF. Playback is at five frames per second, so it is a little choppy; that is the capture rate.

The recordings below were made on build `185b8abd`. They have not been remade for build `be2abf05`, so a control may have moved since; the guides say which build each picture is from.

There is no recording of the Agent tab and none of the Hour view: a live session or a live hour prints local paths. Their pictures, and the pictures of Train, Library and Research in their guides, are offscreen renders (`ember-studio monitor --render-png`) on made-up data, drawn by build `be2abf05`; see [how the pictures were made](../tabs/train.md#how-the-pictures-were-made). Guides: [Agent](../tabs/agent.md), [Train](../tabs/train.md), [Hour view](../tabs/hour-view.md), [Library](../tabs/library.md), [Research](../tabs/research.md).

| Recording | What it shows | mp4 | gif | Size (mp4 / gif) |
| --- | --- | --- | --- | --- |
| tour | Tabs 01 to 08 in turn (Console and Agent left out: their live content is not published) | [tour.mp4](tour.mp4) | [tour.gif](tour.gif) | 388 KB / 412 KB |
| train | Train: RAW, MIXED EMA, SOURCES; the CURVE and POWER rail buttons taking a chart across the canvas | [train.mp4](train.mp4) | [train.gif](train.gif) | 341 KB / 1019 KB |
| library | Library: sort NEWEST and SIZE, then ROOM to the list and back | [library.mp4](library.mp4) | [library.gif](library.gif) | 253 KB / 331 KB |
| models | Models: 3B LINEAGE on and off, COMPARE on and off | [models.mp4](models.mp4) | [models.gif](models.gif) | 162 KB / 220 KB |
| evals | Evals: HISTORY on and off, arm and sort controls, selecting the oldest and newest pair | [evals.mp4](evals.mp4) | [evals.gif](evals.gif) | 98 KB / 189 KB |
| weights | Weights: BY LAYER, BY PARAMETER, OLDEST, NEWEST | [weights.mp4](weights.mp4) | [weights.gif](weights.gif) | 64 KB / 105 KB |
| research | Research: experiment buttons, the layer filter L6, L12, L18, all layers, a camera view | [research.mp4](research.mp4) | [research.gif](research.gif) | 278 KB / 427 KB |
| console | Console, cropped to the top: ERRORS ONLY on and off, then JOB STATE | [console.mp4](console.mp4) | [console.gif](console.gif) | 29 KB / 40 KB |
| timeline | Timeline: 24H, ALL, then the LAB and PRESS sources | [timeline.mp4](timeline.mp4) | [timeline.gif](timeline.gif) | 40 KB / 89 KB |

All files are under 10 MB.
