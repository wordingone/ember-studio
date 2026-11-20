# Job receipt

A job receipt is a JSON record that the lab or Studio writes about one job, before or after the job runs. The program writes five shapes of it. [`job-receipt.schema.json`](job-receipt.schema.json) describes all five in one schema: a document is valid when it is exactly one of them.

| Shape | Written by | Where it is written | `schema` or `event` word |
| --- | --- | --- | --- |
| Operational receipt | The lab, when asked to export one | A file the caller names (verb `export_receipt`), or a content-addressed file in a folder the caller names (verb `export_content_addressed_receipt`) | `ember-lab-operational-receipt-v1` |
| Start receipt | The lab, when it starts a job of kind `hour`, `learn` or `dream` | Next to the job's log, as `<log>.lab-start.json` | `ember-lab-hour-start-v1` |
| Inspect intent receipt | The lab, when it starts a job of kind `inspect` | `receipt-intent.json` in the job's folder under the lab's log folder | `ember-lab-job-intent-v1` |
| Inspect terminal receipt | The lab, when an `inspect` job ends | `receipt-terminal.json` in the same folder | `ember-lab-job-terminal-v1` |
| Press receipt row | Studio, for each step of Start and Stop | One JSON line of the press receipts file (`press-receipts.jsonl`), appended before the step is taken | `event`: `pressing`, `started`, `refused`, `stop_requested`, `stopped` |

Examples that validate against the schema: [operational](examples/job-receipt.example.json), [start](examples/job-receipt.start.example.json), [inspect intent](examples/job-receipt.inspect-intent.example.json), [inspect terminal](examples/job-receipt.inspect-terminal.example.json), [press row](examples/job-receipt.press-refused.example.json). The paths in the examples are neutral; a real receipt holds the paths as the lab was given them.

## Operational receipt

The lab's record of one job, read back from the lab's own job table. Only a job in a terminal state (`stopped`, `exited` or `failed`) can be exported as a content-addressed receipt; the other export verb has no such limit.

| Field | Meaning |
| --- | --- |
| `schema` | `ember-lab-operational-receipt-v1` |
| `ember_lab_identity` | `binary_sha256`: the sha256 of the lab program that wrote the receipt. `source_sha256`: the source identity the lab carries. |
| `job_id` | The job's id. |
| `identity_sha256` | The sha256 the job's identity was bound to before it started (for a script kind, the script's). |
| `resource_lease` | The lease the job held: `hour-chain` for the card kinds, `cpu-lane` for the cpu kinds. |
| `state` | One of `starting`, `prepared`, `running`, `stopping`, `orphaned`, `identity_conflict`, `stopped`, `exited`, `failed`. |
| `pid` | The process id of the job. |
| `executable_identity` | The identity of the program file the job ran, as the lab recorded it. |
| `restart_policy` | Always `never`. |
| `exit_code` | The exit code, or `null` while there is none. |
| `logs` | `stdout` and `stderr`, each `{file_name, sealed, sha256}`. When the lab has sealed the log, `sealed` is true and `sha256` is the hash of the file; otherwise `sealed` is false and `sha256` is `null`. |
| `events` | The job's event log, oldest first: rows of `{seq, ts_ms, kind, payload}`. `kind` names the event (for example `job_start_reserved`, `job_prepared`, `job_started`, `job_stop_requested`); the shape of `payload` depends on the kind. |
| `outage_events` | The planned-outage events of the job's lease, in the same row shape. |
| `scientific_capability_evidence` | Always `false`: the receipt says what ran, not what the run proved. |

## Start receipt

Written twice, to the same file. First, with `phase` set to `intent`, before the job's process exists: the file is created new, so a second start with the same log is refused. Then, when the job is running, it is rewritten with `phase` set to `started`, and `pid` and `started_at_ms` added. If that second write fails, the job still runs, the `intent` file stays on disk, and the start reply says `receipt_complete: false`. `start_tail_error` is added only when something failed after the job began to run.

| Field | Meaning |
| --- | --- |
| `schema` | `ember-lab-hour-start-v1` |
| `kind` | `hour`, `learn` or `dream`. |
| `job_id`, `attempt`, `base_job_id` | The job's id, which attempt of this request it is (1 or more), and the id attempt 1 takes. A request is the same script sha256 and the same log path. |
| `script`, `sha256` | The script and the sha256 of its bytes that the lab checked. |
| `log`, `bash`, `cwd` | The log path, the shell and the working directory (`null` when none was named). |
| `redirect` | The shell text that runs the script and sends its output to the log. |
| `env_key_count`, `env_sha256` | How many environment variables the job got and a fingerprint of them. The values are never written. |
| `daemon_pid`, `daemon_priority_class`, `daemon_affinity_mask`, `daemon_system_mask` | What the lab itself ran with when it started the job. The job itself gets normal priority and every processor. |
| `intent_at_ms`, `started_at_ms` | Times in milliseconds since the Unix epoch. |
| `phase`, `pid` | `intent`, or `started` with the job's process id. |

## Inspect receipts

The intent receipt is written before the worker exists. It names the job, the `fingerprint` of the request (checkpoint, parent and grid), the lease (`cpu-lane`), whether the answer already existed (`cache_hit`), the worker program (path and sha256, `null` for a cache hit), how the processors were chosen (`cpu_mask_policy`: `configured` or `inherit`, with `cpu_class_mask`), the request, and the result path.

The terminal receipt ends the job. `outcome` is `published` (the result was written; `result` names its path, sha256 and size), `cache_hit` (the result already existed; `result` as before), `failed` (`code`, `rc` and `detail` give the refusal) or `killed_or_crashed` (the worker ended without writing a terminal receipt; the lab writes one for it when the job's status is read, with `synthesized: true`). Codes and exit codes are in [the command reference](../interface/commands.md).

## Press receipt rows

Studio writes a row before each step so that a record exists of what it asked the lab to do even if the lab never answers. Every row has `event`, `ts` (a time stamp text) and `studio_version`.

| `event` | Written | Fields besides those three |
| --- | --- | --- |
| `pressing` | Before the start request is sent. If it cannot be written, nothing is sent. | `job_kind` (`hour` or `learn`), `script`, `sha256`, `log`, `cwd`, `bash`, `env_keys` (a count), `pipe` |
| `started` | After the lab accepted the start. | `job_kind`, `job_id`, `pid`, `script`, `sha256`, `log`, `lab_receipt` (the start receipt's path), `bash`, `cwd`, `pipe` |
| `refused` | After a start did not go. | `script`, `sha256`, `log`, `kind`, `refusal_code`, `rc`, `detail`, `reason`. `kind` is `refused` (the lab's refusal, with its code and exit code), `unreachable`, `no_reply`, `bad_pipe_name`, `too_large`, `protocol`, `rpc_error`, or `studio` when Studio's own checks refused before sending anything (no code, `reasons` lists every reason). |
| `stop_requested` | Before the stop request is sent. | `job_id`, `pipe` |
| `stopped` | After the lab answered. | `job_id`, `accepted`, `state`, `exit_code` |

A line that is not JSON is counted and skipped by the reader, never fatal. A `started` row written before job kinds existed has no `job_kind` and was an hour; the schema asks for the member because Studio writes it today.
