<!-- Generated from the program source by the release pipeline; do not edit by hand. Open an issue to request a change. -->

# Command reference

*Generated from the program source by the release pipeline; do not edit by hand. Open an issue to request a change.*

Every command an agent or a script can send: the 40 verbs of the lab's wire protocol, the one streaming verb, and the verbs and flags of the `ember-studio` program. A machine-readable form is [`commands.schema.json`](commands.schema.json). For the files these commands read and write see [file formats](../formats/README.md); for how to drive the window without taking the keyboard focus, see the [command line page](../command-line.md).

## The lab's wire protocol

JSON-RPC 2.0 over a named pipe: `ember-lab serve --pipe \\.\pipe\NAME` listens, and a client opens that pipe.

- One request is one line of JSON, at most 65536 bytes. The lab answers with one line.
- A request is `{"jsonrpc":"2.0","id":1,"method":"ping"}`, with `"params":{...}` when the verb takes any. A reply is `{"jsonrpc":"2.0","id":1,"result":{...}}` or `{"jsonrpc":"2.0","id":1,"error":{"code":N,"message":"...","data":...}}`.
- The client must run as the same user as the lab, or every verb is refused with -32001.

### Error codes

| Code | Name | Meaning |
| --- | --- | --- |
| -32700 | `parse_error` | The line is not JSON. |
| -32600 | `invalid_request` | The line is JSON and not a JSON-RPC 2.0 request. |
| -32601 | `method_not_found` | The `method` is not one of the verbs. |
| -32602 | `invalid_params` | The `params` do not fit the verb. |
| -32000 | `operation_failed` | The verb failed. `data` is the text of the lab's error (its variant name and fields). |
| -32001 | `hour_refused_or_foreign_user` | A start was refused, or the client is not the user that owns the lab. A refusal's `data` is `{refusal_code, rc, detail}` and `message` is `hour_refused` or `lab_job_refused`; for a foreign user `message` is `client user does not own this ember-lab` and there is no refusal code. |
| -32002 | `turn_refused` | An agent turn was refused. `data` is `{refusal_code, detail}`. |

### Job states

A job is in one of: `starting`, `prepared`, `running`, `stopping`, `orphaned`, `identity_conflict`, `stopped`, `exited`, `failed`. The restart policy is always `never`. `stopped`, `exited` and `failed` are the terminal states.

## Verbs of the lab

Forty verbs. A verb with no `params` column takes none. Reply members are the ones the lab sends.

| Verb | What it does | Params | Reply |
| --- | --- | --- | --- |
| `capabilities` | What this lab build offers. | none | `{schema, build, verbs, streams, resident, tabs, models}` |
| `ping` | Is the lab alive. | none | `{status: ok}` |
| `runtime_identity` | Which lab program is answering. | none | `{schema_version: ember-lab-runtime-identity-v1, pid, ...}` |
| `wall_observation_snapshot` | Read the resource-wall observations recorded after two sequence numbers. | `after_vram_seq`, `after_disk_seq` | A snapshot: `schema_version, captured_at_ms, next_vram_seq, next_disk_seq, daemon_identity, vram_observations[], disk_observations[]` |
| `bind_identity` | Bind a file's sha256 as the identity of a job. | `job_id`, `path`, `sha256` | `{bound: true}` |
| `register_schedule_prediction` | Record what a job is predicted to take, before it runs. | `job_id`, `artifact_class`, `predicted_duration_ms`, `predicted_tokens`, `predicted_program_completion_ms`, `absolute_deadline_ms` | `{registered: true}` |
| `record_schedule_measurement` | Record what a job measured, against its prediction. | `job_id`, `measured_duration_ms`, `measured_tokens`, `outcome`, `receipt_sha256` | `{recorded: true}` |
| `write_schedule_alarm_state` | Write the schedule alarm state to a file. | `path` | `{written: true}` |
| `acquire_lease` | Take a named resource lease for a job. | `resource`, `job_id` | `{acquired: true}` |
| `dispatch_manifest` | Start a job from a dispatch manifest after the lab's preflight. | `manifest_utf8`, `manifest_sha256` | `{pid, preflight_receipt_path, preflight_receipt_sha256}` |
| `resource_guard_rearm` | Re-arm a resource guard that a diagnostic receipt froze. | `frozen_observation_sha256`, `breach_class`, `diagnostic_receipt_path`, `diagnostic_receipt_sha256` | `{path, sha256}` of the re-arm receipt |
| `consume_verifier_dispatch_token` | Spend a one-time dispatch token. The caller's process id must be one the lab can read from the pipe. | `job_id`, `token` | `{consumed: true, daemon_identity: {schema_version, pid, binary_sha256, source_sha256}}` |
| `supervise_server_cycle` | Run one supervised model-server cycle against an authority file. | `authority_path`, `authority_sha256`, `receipt_path`, `restore_manifest_path`, `serving_contract_path`, `serving_contract_sha256`, `required_headroom_bytes`, `now_ms` | The cycle receipt |
| `start_hour` | Start a script job (the older, hour-shaped form of start_lab_job). | `kind`?, `script`, `sha256`, `log`, `cwd`?, `bash`?, `env` | `{kind, job_id, pid, script, sha256, log, receipt_path, bash, cwd, receipt_complete, receipt_error?, start_tail_error?}` |
| `check_hour` | Run every refusal check of start_hour and create nothing. | `kind`?, `script`, `sha256`, `log`, `cwd`?, `bash`?, `env` | `{kind, job_id, script, sha256, log, receipt_path, bash, cwd}` |
| `check_lab_job` | Check a start request of any built kind and create nothing. `kind` picks the shape: hour, learn or dream take the script shape, inspect takes the inspect shape. Refusal message `lab_job_refused`. | a script body or an inspect body (below) | The kind's checked shape |
| `start_lab_job` | Start a job of any built kind. Same body as check_lab_job. | a script body or an inspect body (below) | The kind's started shape (script kinds: as start_hour) |
| `lab_job_status` | The state of a job of any kind, with its receipts. | `job_id` | `{job_id, kind, class, state, cache_hit, job_dir, intent, terminal, result}` |
| `job_events` | A page of a job's event log. | `job_id`, `after_seq`?, `limit`? | `{events: [{seq, ts_ms, kind, payload}]}` |
| `list_jobs` | The script jobs (hour, learn, dream) in the lab's own table, newest start first. Params are optional. | `limit`? | `{jobs: [{job_id, kind, state, started_at_ms, exited_at_ms, exit_code, script, log}]}` |
| `job_state` | The state word of a job. | `job_id` | `{state}`, or a null result for an unknown job |
| `stop_job` | Ask the lab to stop a job. | `job_id` | `{stopped: true}` |
| `export_receipt` | Write the job's operational receipt to a new file. | `job_id`, `path` | `{exported: true}`; refuses a path that exists |
| `export_content_addressed_receipt` | Write the operational receipt into a folder under its own sha256. Terminal states only. | `job_id`, `directory` | `{path, sha256}` |
| `export_assessment_evidence` | Write the evidence bundle of a finished job. The directory must not exist. | `job_id`, `directory` | An artifact object |
| `plan_outage` | Plan an outage window on a resource. | `resource`, `starts_at_ms`, `ends_at_ms`, `reason` | `{outage_id}`; refused when the end is not after the start |
| `cancel_outages` | Cancel the planned outages of a resource. | `resource` | `{cancelled: n}` |
| `job_exit_code` | A job's exit code. | `job_id` | `{exit_code}` (integer or null) |
| `job_result` | A job's exit code and captured output. | `job_id` | `{exit_code, stdout, stderr, stdout_encoding, stderr_encoding, stdout_sha256, stderr_sha256}` |
| `issue_run_certificate` | Issue a run certificate from a certificate document. | `certificate_json` | `{certificate_sha256}` |
| `record_launch_context` | Record how the lab was reached when a job was launched. | `job_id`, `daemon_mode`, `daemon_pid` | `{recorded: true}` |
| `record_launch_artifact_refusal` | Record that a launch artifact was refused, with where the evidence is. | `job_id`, `evidence_locator` | `{recorded: true}` |
| `storage_reconcile` | Reconcile storage against a retention policy and a pin set. See docs/formats/pin-set.md. | `repository_root`, `policy`, `declarations`, `models_root`, `state_root`, `custody`, `pin_set_sha256`, `current_master`, `projected_growth`, `operation` | `{command_identity, authenticated_client_pid, daemon_pid, daemon_binary_sha256, lease_resource, lease_released, daemon_terminal_self_sha256, reopened, execution_receipt}` |
| `paper_compile` | Build a LaTeX paper source. | `source` | A paper status (below) |
| `paper_status` | The state of a paper build. | `source` | `{source, state: none|running|ok|failed, build_dir, started_unix, built_unix, seconds, tex_sha256, pages[], pdf, error_line, log_tail[]}` |
| `agent_turn_submit` | Hand a prompt to the resident agent's seat. | `session`, `text`, `mode`, `cwd` | The turn's queue entry. All four agent_turn verbs refuse with -32002, code `no_worker`, when the lab does not run the seat poller |
| `agent_turn_stop` | Stop the agent's running turn. | `session` | The stop result |
| `agent_turn_status` | The agent's turn state. | `session` | The turn state |
| `agent_turn_unqueue` | Remove a queued turn. | `session`, `id` | `{session, id, removed}` |
| `shutdown` | Ask the lab to stop serving. | none | `{status: shutting_down}` |

`?` marks an optional member. Hashes are 64 lowercase hex characters. The full parameter shapes are in the schema file.

### Streaming: `agent_live_stream`

One more verb is not among the forty because it does not answer with one line. `agent_live_stream` with `{"session": ...}` answers `{"result":{"stream":"agent_live","version":1}}` and then sends event lines until the stream ends: `{"event":"live","version":V,"text":...}` carries the agent's text so far, `{"event":"end","version":V}` ends the stream and `{"event":"ping"}` keeps it alive.

### The request bodies of `check_lab_job` and `start_lab_job`

`kind` picks the shape. For `hour`, `learn` and `dream` (the default is `hour`): `script`, `sha256`, `log`, `env`, and optionally `cwd` and `bash`; a `learn` request may add `method` (`full`, `lora` or `qlora`). For `inspect`: `checkpoint`, and optionally `parent` and `grid` (1 to 64). `start_hour` and `check_hour` take the script shape. See the [job kind manifests](../../manifests/kinds) for the rules of each kind.

## Refusals

A refused start carries a refusal code and an exit code `rc`. Studio's `press` and the `ember-lab` command line exit with the `rc`. A code that no table names exits 99.

### Hour, learn and dream starts

| Code | rc |
| --- | --- |
| `hour_path_relative` | 20 |
| `hour_script_name` | 21 |
| `hour_script_missing` | 22 |
| `hour_sha_malformed` | 23 |
| `hour_sha_mismatch` | 24 |
| `hour_log_exists` | 25 |
| `hour_log_unwritable` | 26 |
| `hour_bash_refused` | 27 |
| `hour_env_ember_key` | 28 |
| `hour_env_invalid` | 29 |
| `hour_child_priority` | 30 |
| `hour_child_affinity` | 31 |
| `hour_lease_conflict` | 32 |
| `hour_receipt_exists` | 33 |
| `hour_receipt_write` | 34 |
| `hour_spawn_failed` | 35 |
| `hour_cwd_invalid` | 36 |
| `hour_kind_unknown` | 37 |

### Inspect starts

| Code | rc |
| --- | --- |
| `inspect_path_relative` | 40 |
| `inspect_checkpoint_missing` | 41 |
| `inspect_checkpoint_format` | 42 |
| `inspect_checkpoint_incomplete` | 43 |
| `inspect_checkpoint_in_flux` | 44 |
| `inspect_parent_same` | 45 |
| `inspect_parent_no_overlap` | 46 |
| `inspect_grid_invalid` | 47 |
| `inspect_worker_missing` | 48 |
| `inspect_lease_conflict` | 49 |
| `inspect_receipt_write` | 50 |
| `inspect_spawn_failed` | 51 |
| `inspect_checkpoint_changed` | 52 |
| `inspect_read_failed` | 53 |
| `inspect_result_write` | 54 |
| `inspect_cancelled` | 55 |
| `inspect_cpu_placement` | 56 |

### Kind and method

| Code | rc |
| --- | --- |
| `lab_kind_not_built` | 38 |
| `lab_request_invalid` | 39 |
| `lab_pretrain_off` | 120 |
| `lab_method_unknown` | 121 |

### Approved presses

| Code | rc |
| --- | --- |
| `press_not_listed` | 100 |
| `press_line_malformed` | 101 |
| `press_bar_changed` | 102 |
| `press_predictions_changed` | 103 |
| `press_duplicate` | 104 |
| `press_id_invalid` | 105 |
| `press_approved_missing` | 106 |
| `press_job_not_found` | 107 |
| `press_state_unwritable` | 108 |
| `press_cancel_refused` | 109 |
| `press_checker_refused` | 110 |
| `press_checker_unavailable` | 111 |
| `press_minutes_unknown` | 112 |
| `press_over_minutes` | 113 |
| `press_queue_full` | 114 |

## The `ember-studio` program

Verbs that open no window. Each prints to the terminal and returns an exit code; with `--json` where listed the output is one JSON document.

| Usage | What it does | Exit codes |
| --- | --- | --- |
| `ember-studio press --script P --sha256 H --log L [--kind hour\|learn] [--check] [--json]` | Ask ember-lab to start an hour or a learn job. `--check` runs only the preflight. | 0 started, 2 refused, 3 bad arguments, 4 failed |
| `ember-studio status [--job ID] [--log L \| --set-dir D] [--json]` | The lab's state of a job and what its log says, in words. | 0 read, 2 nothing to read |
| `ember-studio stop [--job ID] [--yes] [--json]` | Ask the lab to stop a job. | 0 ended, 2 refused, 4 failed, 6 not confirmed, 7 not ended |
| `ember-studio ui-tree --live` | Read the RUNNING window's tab (through the instance pipe: no focus, no restore, no UI Automation). One line: `{"live":true,"pid":N,"tab":SLUG,"frame":N,"age_ms":N}`; `age_ms` is how old the last drawn frame is. Plain `ui-tree` never reports the running window. | 0 ok, 1 no Studio running |
| `ember-studio ui-tree [--json] [--mode SLUG] [--agent-stub SCENARIO]` | Draw the window offscreen and print every control: name, role, value, disabled. It does not read the running window; it draws a fresh one. | 0 ok, 3 bad arguments |
| `ember-studio ui-sweep [--json]` | Operate every control offscreen and list the ones that do nothing. | 0 no dead control, non-zero otherwise (the report lists each) |
| `ember-studio monitor --headless --json` | One snapshot of the hour telemetry as JSON. | 0 ok, 2 no source, 3 bad arguments |
| `ember-studio monitor --render-png FILE [--size WxH] [--mode SLUG] [--select KEY] ...` | Draw the real UI offscreen and write a PNG plus a JSON render receipt on stdout. | 0 ok, 3 bad arguments, 4 render failed |
| `ember-studio windows [--pid N]` | The visible top-level windows of the running Studio. | 0 exactly one visible window (the main window) |
| `ember-studio selftest-repaint [--seconds N]` | Draw frames with no input and prove the on-screen clock moves. | 0 pass, 1 fail, 3 bad arguments |

`ui-tree --json` is a JSON array of `{name, role, value, disabled}`; `role` is one of `Button`, `TabItem`, `CheckBox`, `TextInput`, `MultilineTextInput`, `Caption`, `Image`, `ListItem`. `value` is `null` for a button. `ui-tree --live` reads the running window and is read-only.

### Operating the running window

There is only one Studio window. A second launch hands its request to it, prints `STUDIO_ALREADY_RUNNING pid=<n>` and exits.

| Flag | What it does |
| --- | --- |
| `--act NAME` | Operate the control `NAME` as an accessibility Click, inside the window's own event loop (no UI Automation call, no OS input, no focus change). Several `--act` flags run in order. |
| `--read-tab` | Read-only: the reply carries the tab the window drew last. The window is not woken, restored or handed anything. `ui-tree --live` uses it. |
| `--act-set NAME VALUE` | Fill the text input `NAME`. The value is taken as given, even if it starts with `--`. Allowed names: see section 3. Any other name is refused, nothing is applied, exit 5 (`ACT_SET_REFUSED`). |
| `--act-clear NAME` | Empty the text input `NAME` (for callers that cannot pass an empty argument). |

A flag exits 0 once the request is handed over; the window applies it on its next frame (allow two to three seconds), and the effect is read afterwards from state. `--act` and `--act-set` change the window, so run them only against a Studio started for the purpose. `--act NAME` with no Studio running: not verified here (the program's two pages say different things).

### Names `--act-set` accepts

`agent.input`, `agent.folder`, `agent.dock.input`, `agent.newcmd.name`, `agent.newcmd.description`, `agent.newcmd.args`, `agent.newcmd.template`, `press.script`, `press.sha256`, `press.log`, `train.method`, `research.project.folder`, `research.project.name`, `research.project.open_path`, `research.project.title`, `research.project.question`, `research.project.experiment.title`, `research.project.experiment.kind`, `research.project.experiment.spec_path`, `research.project.experiment.bar_path`, `research.project.hypothesis.text`, `research.project.model.role`, `research.project.model.name`, `research.project.model.path`. Any other name is refused, nothing is applied, and the exit code is 5 (`ACT_SET_REFUSED`).
