# Job kind manifest

**The program has no file called a job kind manifest.** The lab does not read one and does not write one. The list of job kinds is a table that is compiled into the lab. Each kind in it has a lease class, a prefix for its job ids, and a range of exit codes that only its refusals use.

This page and [`job-kind-manifest.schema.json`](job-kind-manifest.schema.json) define a **descriptive** record of one kind, written from that table, so that a person or an agent can read what a kind is without running the lab. Nothing consumes these files. The word `ember-job-kind-manifest/1` is a label this repository gives to the description; it is not a schema word of the program. A manifest here is only as current as the build it was written from: if a manifest and a running lab disagree, the lab is right, and the interface reference ([commands](../interface/commands.md)) is the generated record.

- Valid example: [`examples/job-kind-manifest.example.json`](examples/job-kind-manifest.example.json).
- The manifests of the kinds the lab can run today: [`hour`](../../manifests/kinds/hour.json), [`learn`](../../manifests/kinds/learn.json), [`dream`](../../manifests/kinds/dream.json) and [`inspect`](../../manifests/kinds/inspect.json).

## The kind table

| Kind | Lease class | Lease | Exit codes of its refusals | Runnable today |
| --- | --- | --- | --- | --- |
| `hour` | `card` | `hour-chain` | 20 to 37 | yes |
| `learn` | `card` | `hour-chain` | 20 to 37 | yes |
| `dream` | `card` | `hour-chain` | 20 to 37 | yes |
| `inspect` | `cpu` | `cpu-lane` | 40 to 59 | yes |
| `construct-check` | `cpu` | `cpu-lane` | 60 to 79 | no |
| `capture` | `card` | `hour-chain` | 80 to 89 | no |
| `eval` | `card` | `hour-chain` | 90 to 98 | no |

The lease class belongs to the kind and is never a flag of a request. Every `card` kind takes the one `hour-chain` lease, so one card job runs at a time on the shared card. A `cpu` kind takes the separate `cpu-lane` lease and never reads, takes or releases the card lease, so a live card job can neither cause nor suffer a cpu-kind refusal.

A request for a kind that is in the table and not runnable is refused `lab_kind_not_built` (exit code 38). A request for the kind `pretrain` is refused `lab_pretrain_off` (120) whatever else it holds: pretraining is off because it needs far more compute than this machine has. An unknown kind is refused `hour_kind_unknown` (37). There are no manifests for `construct-check`, `capture` and `eval`: they are names in the table with nothing behind them yet.

## Fields

| Field | Meaning |
| --- | --- |
| `format` | `ember-job-kind-manifest/1` |
| `kind` | One of the seven names of the table. |
| `summary` | One plain sentence. |
| `lease_class`, `lease_resource` | `card` with `hour-chain`, or `cpu` with `cpu-lane`. |
| `job_id_prefix` | A job id starts with this word and a dash. |
| `refusal_exit_codes` | `{min, max}`: the exit codes only this kind's refusals use. 99 means a code no table names and is never used by a table row. |
| `built` | Whether the lab can run the kind. |
| `verbs` | The lab verbs that take the kind (the reference lists every verb). |
| `script_name_rule` | For a kind that runs a script: the file name rule. |
| `request` | The members of the request body: `name`, `type`, `required`, `meaning`. |
| `environment` | Variables the lab adds to the job's environment for this kind. |
| `writes` | Files the lab or the job writes. |
| `refusal_codes` | The refusal codes of the kind's own table, each with its process exit code. |

## What the three script kinds have in common

`hour`, `learn` and `dream` run one script under the card lease. The request names the script, the sha256 of its bytes, a log path that must not exist yet, and the job's exact environment; the lab refuses a script whose bytes hash to anything else, a relative path, a log that exists, and any environment variable whose name begins with `EMBER_`. The lab creates the log, writes the [start receipt](job-receipt.md) next to it, and starts the script with the shell's output sent to the log. The kinds differ in the script's file name rule and in the id prefix. A `learn` request may also name a fine-tune method (`full`, `lora` or `qlora`), which the script receives in `LEARN_METHOD`. A `dream` job gets a ledger row when it ends, whatever the script did.

`inspect` is the cpu kind: it reads a checkpoint and writes statistics, and is safe to run beside a card job.
