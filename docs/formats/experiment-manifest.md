# Experiment manifest

In this program the experiment manifest is the **research project file**: a `<name>.ember` file that the Research tab writes and reads. One file holds the question, the hypotheses, the models and the experiments of a project. Each experiment names a frozen spec and a frozen bar by path and sha256. The file is an index and never holds results.

- Schema: [`experiment-manifest.schema.json`](experiment-manifest.schema.json) (word `ember-research/1`).
- Valid example: [`examples/experiment-manifest.example.json`](examples/experiment-manifest.example.json).
- Two ready-to-open manifests: [`locate-then-move.ember`](../../manifests/experiments/locate-then-move.ember) and [`baseline-and-learn.ember`](../../manifests/experiments/baseline-and-learn.ember). They are illustrations: their models are placeholders and the spec and bar files they name do not exist here.

## Who writes it and who reads it

Studio writes it, and only through one function: the whole file goes to a temporary file in the same folder, is flushed, and is renamed over the target, so a crash leaves the old file or the new one, never half of one. Creating a project never overwrites a file of that name. Studio reads it when you open a project, and reopens the last project at the next start. Studio starts no job and writes no other file for a project; it never edits a spec or a bar.

You make one with **File > Create new research project**, or by script: `--act file.new_research_project`, then `--act-set research.project.folder <folder>` and `--act-set research.project.name <name>`, then `--act research.project.new`. You can also write the file by hand; Studio refuses a file that is not JSON or whose `schema` is not `ember-research/1` (`REFUSED_NOT_A_PROJECT`). A file that carries members this schema does not list still opens, and Studio drops those members the next time it saves.

## Fields

| Field | Holds |
| --- | --- |
| `schema` | `ember-research/1` |
| `title` | The project's title; at first the file's name. |
| `question` | The question the project asks. |
| `created_utc` | When the file was made, `YYYY-MM-DDTHH:MM:SSZ`. |
| `hypotheses` | Rows of `id` (`H1`, `H2`, ...), `text` and `status_word` (`open` when added). |
| `models` | Rows of `role` (`donor` or `recipient`), `name`, `path`, `sha256`, `licence_row`. Studio leaves `sha256` empty (hashing a model file would freeze the window); the lab records the hash. |
| `experiments` | Rows described below. |
| `receipts` | A list of text entries; empty when the file is made. |
| `paper` | Optional: `{ "source": <path of a .tex file> }`. The Research tab builds this LaTeX source through the lab and shows its pages. Left out when the project has no paper. |

An experiment row has:

| Field | Holds |
| --- | --- |
| `id` | `e1`, `e2`, ...: the next free one when added; never repeated in a file. |
| `title` | Not empty. |
| `kind` | One of `LOCATE`, `MOVE`, `BASELINE`, `LEARN`. Studio records the kind and any capitalisation is accepted when you add one; the file always holds capitals. What a kind means is the project's own convention. |
| `spec_path`, `spec_sha256` | The frozen spec, written with forward slashes, and its sha256. The sha256 is taken from the file when it can be read at the moment the experiment is added, and is empty otherwise. |
| `bar_path`, `bar_sha256` | The frozen bar, the same way. `bar_path` may end `#<heading>` to name one `## <heading>` section of a spec. |
| `lab_job_ids` | The lab jobs that belong to the experiment. |
| `result_words` | Words that sum up the result. |
| `ruling_path` | The file that holds the experiment's ruling, if one is named. |

## What the Research tab does with it

For each experiment the tab shows the frozen bar verbatim with a status chip that says whether the file still matches the sha256 the project recorded: `INTACT`, `CHANGED SINCE IT WAS FROZEN`, `NO SHA RECORDED`, `NOT READABLE` or `NO BAR DECLARED`. It then shows one card per job in `lab_job_ids`, and the ruling. It only reads: nothing on the page is inferred, and a number that no file declares reads "not declared by the run".

## When Studio refuses to write

The refusal is a line that starts with a code, and nothing is written: `REFUSED_NAME` (empty, over 100 characters, a path separator or a character Windows reserves, a leading dot, a trailing dot or space, or a reserved device name), `REFUSED_FOLDER`, `REFUSED_EXISTS`, `REFUSED_NOT_A_PROJECT`, `REFUSED_NO_PROJECT`, `REFUSED_TITLE`, `REFUSED_HYPOTHESIS`, `REFUSED_MODEL`, `REFUSED_EXPERIMENT` and `WRITE_FAILED` (the old file is unchanged and no temporary file is left).

## Not verified here

The program accepts any text in `role` when it reads a file, and Studio only ever writes `donor` or `recipient`; the schema holds files to what Studio writes.
