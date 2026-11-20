# Capture record

**The program has no file format called a capture record.** There is no schema for one on this page, because there is nothing for it to describe: the lab does not write a capture record, Studio does not read one, and no verb takes or returns one.

What exists nearest to it:

- **A job kind named `capture` is in the lab's kind table and is not built.** It would take the shared card lease and own the refusal exit codes 80 to 89. A request for it is refused `lab_kind_not_built` (exit code 38) and nothing starts. See the [job kind manifest](job-kind-manifest.md) page for the table. When the kind is built, its record will need its own format and this page will change.
- **A flag in the step rows of an hour.** A governed hour writes a `rows.jsonl` file with one JSON row per step, and Studio reads it read-only to draw the hour's curves. A row may carry a member `captured` that is true or false, and Studio shows the latest value as `captured: yes` or `captured: no`. Studio does not write these rows, and what the flag means is defined by the script that writes them, not by this repository, so it is **not verified here** and the schema of a row is not published.

If you need a record of what a job did, use the [job receipt](job-receipt.md).
