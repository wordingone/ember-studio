# How the program is built

This page describes the shape of the program, not its source. The source is in a private repository; this repository holds the documentation, formats, manifests, examples and checks that describe and test the program from outside.

## Two programs and one rule

- **ember-lab** is a resident daemon. It starts, owns, supervises and stops every training run and model server, and it runs the Agent tab's turns. It has no window.
- **Ember Studio** is the window. It is a client of the lab: it asks over a local named pipe and never starts or ends a run itself. See [How Studio talks to ember-lab](lab.md) and the [command reference](interface/commands.md).

The two programs never reference each other's code. What they share lives in a small bottom layer, and the lab and Studio each sit in their own column above it.

## Sixteen packages in three folders

The source tree is one workspace of sixteen packages in four folders. A package may use another only if it is in the same column and sits at a strictly lower rank, or if it is in `shared/`. Equal ranks never use each other, and `lab/` and `studio/` never use each other. The rule is a file that a check reads on every change; a package that breaks it fails the check.

| Folder | Package | Rank | What it holds |
| --- | --- | --- | --- |
| `shared/` | `contract` | 0 | The vocabulary both sides share: the lab's error type, job states and refusal codes. The [commands page](interface/commands.md) is written from it |
| `shared/` | `platform` | 1 | What both sides need from Windows and the machine: the startup CPU pin, processes, paths, hashing, the clock |
| `shared/` | `data` | 2 | Read-only formats and ledgers: the data catalog, the census, the checkpoint index, tensor statistics, storage retention |
| `shared/` | `pipe` | 2 | The lab pipe client: one request and one answer over the named pipe |
| `lab/` | `jobs` | 0 | The job kinds, their receipts and the supervision of a run |
| `lab/` | `model` | 1 | The resident model server: its configuration, launch, the card lock and yield, turn waits, wake markers |
| `lab/` | `agent` | 2 | The resident agent: its loop, tools, approvals, compaction, sessions, hooks, skills, web tools, reviewers and the live channel |
| `lab/` | `ops` | 3 | The lab's operations: mail and loops, press, paper builds, the lab log |
| `lab/` | `app` | 4 | The `ember-lab` program: its command line and the pipe server |
| `studio/` | `kit` | 0 | Building blocks: accessible names, charts, the offscreen renderer, the theme, markdown, widgets, the terminal emulation |
| `studio/` | `client` | 1 | Studio's side of the lab: the pipe client, receipts and the read-only data the tabs draw |
| `studio/` | `pages` | 2 | The frame and the pages: layout, shell controls, selection, tab capabilities, the shared view modes |
| `studio/` | `tabs` | 3 | The tabs: agent, library, models, research, press and training, the embedded terminal panel, the 3D views |
| `studio/` | `app` | 4 | The `ember-studio` program: its command line, single-instance window and control interface |
| `tools/` | `devhost` | | A development host for hot-reloading a panel |
| `tools/` | `xtask` | | The repository's own check and build commands |

## What the repository checks on itself

Every change to the source runs one check command. It refuses a change that:

- breaks the layer rule above;
- grows a source file past its recorded size, or adds a file past the size limit (large files are split by moves that change no behaviour);
- puts a folder path of the build machine in any tracked text file or in a built program (the release build maps those paths out, and a scan reads the finished program);
- reads a record in a tab instead of in `shared/data`, or adds a second way of writing a file atomically, calling the lab pipe, making an HTTP request or starting a hidden child process;
- changes the wire contract without regenerating its schema;
- loses a test by name.

A move and a behaviour change never share a commit.

## What is generated for this repository

The [command reference](interface/commands.md) and its [schema](interface/commands.schema.json) are generated from the program's contract and control interface by the release process; they are never edited by hand here. The [file format](formats/README.md) schemas are written from the program's data types and validated against real files. If a page here disagrees with a released build, the page is wrong: open an issue.
