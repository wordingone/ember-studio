# Mark

**The program has no file format called a mark.** Nothing is written, read or published under that name. This page says what exists nearest to it, so that the name is not looked for in vain.

The nearest thing is the `ember_marks` object that the lab attaches to a message of an Agent session record. A session record is the conversation the Agent tab keeps: a list of messages with a `role` and a `content`. The lab adds `ember_marks` to a message to record what happened around it, so that a session that is resumed draws the same glyphs and the lab can reuse counts it already has. The marks are **never sent to the model**: the lab removes `ember_marks` from every message before it builds a request.

- Schema of the object: [`mark.schema.json`](mark.schema.json). It describes the object only, not the message around it.
- Valid example: [`examples/mark.example.json`](examples/mark.example.json).

## Members

Each member appears only when it applies. No other member is written.

| Member | On which message | Holds |
| --- | --- | --- |
| `skill` | A tool result | The name of the skill that the call activated. |
| `skills` | The wrapper message that a compaction leaves in place of the history | The skills that were active when the history was compacted, so that a later turn can read them back. |
| `approval` | A tool result | What the approval gate ruled on the call: `layer` (a small whole number), `decision`, `reason` and `review_ms` (how long the review took). |
| `hook_block` | A tool result | A hook refused the call: `hook` (its name) and `message`. |
| `ctx_tokens` | An assistant message | The context size the model server counted for that round: its prompt plus its answer, less the thinking tokens that the next request leaves out. The next turn reads the newest value back instead of estimating the size from the text. A compaction replaces the history and so its marks. |
| `ms_prompt_read`, `ms_first_token` | An assistant message | Milliseconds the server took to read the prompt, and milliseconds to the first token it generated; `null` when the server reported nothing. |

A message in a record looks like this, with the mark as one member of it:

```json
{"role": "tool", "tool_call_id": "c1", "content": "ok",
 "ember_marks": {"approval": {"layer": 1, "decision": "allow", "reason": "read-only command", "review_ms": 0}}}
```

## Not verified here

Where the session file sits on disk and how it is named is not described on this page. The Studio window's own notion of a mark on a picture (a node, a bar or a point that can be selected) is a control of the window, not a file; it is covered by the manual.
