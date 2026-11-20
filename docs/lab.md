# How Studio talks to ember-lab

Studio is a client. **ember-lab** is a resident daemon that starts, owns, supervises and stops every training run and model server. Studio never starts or ends a process itself.

## The pipe

Studio and the lab speak JSON-RPC over a Windows named pipe. The default pipe is `\\.\pipe\ember-lab-studio`. Studio takes the part after `ember-lab-` with `--lab-pipe NAME` (the bare name `studio`, or the full pipe name). Each request is one line on its own pipe connection and the reply is one line back. Nothing leaves the machine: the LOCAL · NO CLOUD chip says so. Every verb is listed in the [command reference](interface/commands.md).

## What Studio asks the lab

- `ping`: is the lab there. The Hour view's `ember-lab` check and the Train tab's "lab not answering" use it.
- `capabilities`: which verbs this lab build has, and which tabs it can serve. A tab the lab cannot serve is drawn disabled, with the reason as hover text, and a click does nothing: Train needs the verbs that start, check and list jobs; Console and Timeline need the job events and status verbs; Agent needs the agent turn verbs. Library, Models, Evals, Weights and Research read files and never need the lab for that. A lab with no `capabilities` verb leaves every tab on. This is read from the source and its unit test; it was not run in a live window for this guide.
- Start a job (an hour or a learn job), ask a job's state, exit code and events, list jobs, stop a job. The Hour view, Console and Timeline use these.
- The Agent tab: typed turns in AUTO-REVIEW mode are submitted to the lab (`agent_turn_submit`, `agent_turn_status`, `agent_turn_stop`) and run there, so closing Studio does not cancel one; the other modes run the lab's `agent` command as a child process and read its output, one JSON object per line. The lab also writes a live file for the turn it is running, which Studio hears over one live stream, so a turn the lab starts itself (mail, a loop) draws as it happens. See [Agent](tabs/agent.md).

Studio's own record of what it asked is its **press receipts**, a JSON-lines file written before each step, kept under `%LOCALAPPDATA%\ember-studio` unless `--press-receipts` says otherwise. The Timeline tab draws it.

## What happens when the lab is not there

Studio does not crash. Pages that ask the lab say so in words, for example "the lab did not answer: the pipe does not exist, so the lab daemon is not running". Whatever needs the lab (starting or stopping a job, live job state, the Agent tab's model) does not work without it. The pages that read folders (Library, Models, Weights) are built to read files directly, but that was not checked on a machine that has never had the lab. `ember-studio status --lab-pipe <name of a pipe nobody serves>` prints the same sentence on the command line.

## The GPU card

One GPU is shared. The lab owns it: a job that trains or scores takes the card, and the resident model yields it while a job runs (the Agent tab shows YIELDED, and in modes other than AUTO-REVIEW a message sent then gets a busy-card notice; in AUTO-REVIEW it is queued). Studio itself never touches the GPU, apart from reading its power and utilisation for the Train tab. A model you name in a provider config file runs on your own server and never takes the card.

## Where the lab keeps things, and how to change it

No folder, drive letter or person's name is compiled into the lab. Every folder and tool it uses is a setting, resolved in this order: an environment variable, then a line in the config file, then a default under the lab's own folder in your user profile (`%LOCALAPPDATA%\ember-lab`). A tool that has no sensible default is left unset, and the feature that needs it says which key to set.

- **The config file** is `ember-lab.toml`. The lab looks for the file named by `EMBER_LAB_CONFIG`, else `ember-lab.toml` beside `ember-lab.exe`, else `ember-lab.toml` in its folder under your user profile. It is plain `key = "value"` lines, `[section]` headers and `#` comments.
- **`ember-lab paths`** prints every key with the value it resolved to and where that came from (`env`, `config`, `default` or `unset`). It touches no file and starts nothing.

| Key | Environment variable | What it is | Default |
| --- | --- | --- | --- |
| `card.lock_dir` | `EMBER_CARD_LOCK_DIR` | The folder whose presence is the card lock | `card/card-lock.d` in the lab's folder |
| `card.order_file` | `CARD_ORDER_FILE` | Who may take the card, in order | `card/card-order.txt` |
| `card.requests_dir` | `EMBER_CARD_REQUESTS_DIR` | Yield requests from jobs | `card/card-requests.d` |
| `press.approved`, `press.kill_receipts`, `press.gpu_window_marker` | | The approved-presses list, the kill receipts, the marker file for a GPU window | `press/...` |
| `press.checker`, `press.verdict_checker` | | Commands that check a press and its verdict | unset |
| `resident.server_exe`, `resident.turbo_exe`, `resident.chat_template`, `resident.model` | `EMBER_AGENT_DEFAULT_SERVER_EXE`, `EMBER_AGENT_DEFAULT_MODEL` | The resident model's server program, its template and the model file. This is where "model locations" are set | unset |
| `reviewer.model` | | The model the AUTO-REVIEW reviewer uses | unset |
| `seat.home` | | The agent's own folder: its sessions, its server file, its `opencode.json` | `seat` in the lab's folder |
| `tools.bash`, `tools.agent_bash`, `tools.curl`, `tools.miktex_bin` | `EMBER_CURL` | Programs the lab or the agent calls | unset (`curl` falls back to the one in the system folder) |
| `web.private_terms` | `EMBER_PRIVATE_TERMS` | A list of words the agent's web tools must not send out | unset: no list is read, and the web tools check email addresses only. A list that is named and cannot be read closes the web tools |
| `custody.drive` | `EMBER_CUSTODY_DRIVE` | The drive a custody check uses | unset: every custody argument is refused until you name one |
| `mail.db`, `mail.signals`, `mail.founders`, `mail.recipient` | | Where the lab reads mail that starts agent turns | `mail/...` in the lab's folder |
| `slash.folder`, `slash.config_dir` | | Where slash commands live | `.ember`, unset |
| `lab.log_dir` | | The lab's log folder | `logs` |
| `dream.ledger`, `seat.loops_validator`, `discord.recent_cmd`, `discord.ember_webhook_id` | | Optional integrations (an unset dream ledger falls back to a file under the seat folder) | unset |

Every key has an environment variable of its own; the table names the ones used elsewhere in these docs. The table lists the keys of the lab program built from the current source (read from it and from the output of `ember-lab paths` on that build, run with an empty profile, so every default shown is under a scratch folder).

## Settings that are not folders

- **The resident model's server line** (program, model, context, cache types, batch sizes, port, sampling, thinking budget, answer limit) comes from one file, `.ember/server.json` in the seat folder; `EMBER_AGENT_SERVER_CONFIG` names another file, or `off` for none. A file that is present and not valid stops the start instead of falling back silently.
- **Idle sleep**: `sleep_idle_seconds` in that file is how many idle seconds pass before the resident model releases the card. The built-in default is 20 seconds; `0` means it never sleeps.
- **Any model**: a provider config file, described in [Agent](tabs/agent.md#choosing-the-model).
- **Compaction size**: `EMBER_AGENT_COMPACT_AT`, described in [Agent](tabs/agent.md#long-sessions-compaction).

## What this build ships

No release has been published yet, so there is no download of either program. The lab is built from the same source as Studio and no longer contains paths to anyone's machine (see above), but it has not been released, and Studio does not need you to have one: it opens, reads the folders you point it at and says in words that the lab is not answering. The lab is Windows-only today; see [platforms](platforms.md) and [known limits](known-limits.md).
