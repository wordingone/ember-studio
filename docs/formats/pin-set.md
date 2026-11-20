# Pin set

The pin set is the **declarations file** of the lab's storage reconciliation: a JSON array in which an operator names, file by file, what the storage census must treat as protected and what it may reclaim. The lab never guesses a file's standing: a file the census finds that the pin set does not declare is recorded as `unknown`, and a census with any `unknown` row refuses to produce a plan.

- Schema: [`pin-set.schema.json`](pin-set.schema.json)
- Valid example: [`examples/pin-set.example.json`](examples/pin-set.example.json)

## Who writes it and who reads it

An operator or a tool writes it; the lab only reads it. The verb `storage_reconcile` (and the lab command `storage-reconcile` that sends it) takes the file's path as `declarations` and **the sha256 of its raw bytes** as `pin_set_sha256`. The lab hashes the file again and refuses the request when the two differ, so the hash is the pin set's identity: change one byte and it is a different pin set. The hash is carried into the plan and into every receipt the reconciliation writes, and the lab re-reads the file for a resumed run and refuses it if the hash moved.

The pin set is one of four inputs. The others are a policy file (word `ember-storage-retention-policy-v1`: the two custody classes, their roots, quotas and the ordered protected and eligibility rules), the two class roots on disk, and the current revision of the repository's remote master. The operation is `dry-run`, `commit`, `resume` or `rollback`. A dry run builds the plan and removes nothing.

## Fields

The file is an array. Each element is one declaration; no member other than these is allowed.

| Field | Meaning |
| --- | --- |
| `class` | `models` or `state`: which custody class's root the path is under. |
| `relative_path` | The file, relative to the class root, with forward slashes. Not empty, not absolute, no backslash, no `.` or `..` component. Two declarations that differ only by letter case are the same declaration, and the lab refuses the duplicate. |
| `disposition` | `protected`, `reproducible`, `terminal_compressible`, `duplicate_reclaimable`; and the four refusal words `unknown`, `path_escape`, `reparse_point` and `hardlink_ambiguous`. The lab itself puts these four on a path it cannot rule on; a census containing any of them refuses to plan. |
| `pin_reasons` | A list of reasons the file is pinned. A reason may not be empty. |
| `checkpoint` | `null`, or `{series, sequence}` (a non-empty series name and a sequence of 1 or more) for a file of a checkpoint in the `models` class. All files of one `{series, sequence}` must sit in one folder. |
| `duplicate_witness` | Required for `duplicate_reclaimable` and `null` or absent for every other disposition. It names the copy that is kept: `retained_relative_path`, `retained_raw_sha256`, `retained_physical_identity`, `authority_identity`, and `independently_reopened`, which must be true. The kept copy must itself be declared `protected`, must hash to `retained_raw_sha256`, and must be a different physical file. |
| `terminal_kernel_witness` | Required for `terminal_compressible` and `null` or absent for every other disposition: `retained_relative_path`, `retained_raw_sha256`, `receipt_identity`, and `independently_reopened`, which must be true. |

`retained_physical_identity` is the operating system's identity of the file's storage: `windows:<8 lowercase hex>:<16 lowercase hex>` or `unix:<device digits>:<inode digits>`. Every hash is 64 lowercase hex characters. The three members `checkpoint`, `duplicate_witness` and `terminal_kernel_witness` may be left out or `null`.

## How the lab treats a declaration

The lab walks both class roots. Each file found takes the standing the pin set declared for it, together with its byte count, its sha256, its physical identity and its modification time, which the lab observes itself. Three cases are not decided by the pin set. A file the pin set does not declare is `unknown`. A symbolic link or a reparse point is `reparse_point`. A file with more than one hard link is `hardlink_ambiguous`. Any of these rows, or a `path_escape` row, makes the lab refuse to plan. A declaration whose file is not found, and a declaration repeated under a different letter case, also refuse the census. The plan that follows is bound to the hash of the policy and to the hash of this file.

## Not verified here

The shape of the plan and of the execution receipt that a reconciliation writes is not described on this page.
