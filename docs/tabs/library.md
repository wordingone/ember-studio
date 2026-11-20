# 02 Library

The data the lab holds, as a place you can look around. The room and list pictures were drawn by build `de6494fe` on made-up data (see [how the pictures were made](train.md#how-the-pictures-were-made)); the selected-pack picture is from `edb7d3ad` and the recording from `185b8abd`.

## What it shows

The page reads the data packs under the lane root (`--data-root` or `EMBER_LANE_ROOT`, reading `<DIR>/packed/*`) and re-reads every 4 seconds while the tab is open. Two views of the same packs.

**Room** (the default when the lane root holds packs): a 3D reading room of bookcases. Each row of stacks is one modality (text, audio, image and so on), with a sign at its end that names the modality and its size in GiB; the row's length follows its GiB, so the row with the most data is the longest. A pack is a book (a pack too long for one spine is a set of volumes, and a small one a pamphlet); a book with a pale outline is on the Hugging Face hub only, and a glowing one is arriving. The **HUD** at the top left counts the books and their size, splits them into local, hub and arriving, and, once something has arrived since the window opened, draws a strip of its growth. The HUD button at the top right opens a table of how much is where. With nothing selected the right panel lists the packs as bars with their sizes.

![The room on made-up packs: one row, one sign, and the HUD](../media/library-room.png)

In the picture the made-up packs are shelved under a single sign, HELD-OUT; made-up folders carry no modality, so it does not show the several rows a real library has. The room needs no GPU in an offscreen render: it is drawn by a software twin.

Selecting a book shows the pack in the right panel: its name, a bar for its bytes, a bar for its file count, and how long ago its newest file changed. This picture is from the earlier room and was not redrawn:

![A pack selected: bytes, files and the age of the newest file (build edb7d3ad)](../media/library-pack.png)

The selection in this picture was made with the render verb (`--select pack:NAME`, see [command line](../command-line.md)); picking a book with the mouse in the window was not exercised.

**List**: one bar per pack folder, sorted by size, with the pack's name and its size. The header counts pack folders, files and bytes and gives the newest file's time.

![The list view](../media/library-list.png)

If no lane root is configured the page says so and names the flag: `no lane root is configured: pass --data-root DIR or set EMBER_LANE_ROOT`. Without a flag Studio also looks for a conventional place on a drive of the machine it runs on; on another machine it finds none and the page says which flag to give.

## Controls

| Group | Control | What it does |
| --- | --- | --- |
| PACKS | RESCAN | Reads the folders again now |
| PACKS | ROOM | Switches between the room and the list |
| SORT | NEWEST / SIZE | Orders the packs by newest file or by size; the right-hand list follows. SIZE is disabled, with `already sorted by size: choose Newest to change the order`, while the list is already sorted by size |

## A typical task: find what the largest packs are

1. Open Library. Press ROOM until the list shows (ROOM is on while the room is drawn).
2. Read down the bars: the longest bar is the largest pack. Names are the pack folder names.
3. Press NEWEST to reorder by newest file, and RESCAN after you add packs.
4. Press ROOM again to return to the room.

![Recording: room to list and back, with the sort changing](../media/library.gif)

*Recording: [library.mp4](../media/library.mp4), made on build `185b8abd`.*

## Known limits of this tab

- The tab has no control that opens what is inside a pack. The separate `ember-studio library` command has `open` (decode one page of a pack) and `provenance` (what the newest hour read); they are described by the program's own help text and were not run for this guide.
- Panning and zooming the room with the mouse, and the HUD button, were not exercised.
