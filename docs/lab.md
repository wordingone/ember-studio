# How Studio talks to ember-lab

Studio is a client. **ember-lab** is a resident daemon that starts, owns, supervises and stops every training run and model server. Studio never starts or ends a process itself.

## The pipe

Studio and the lab speak JSON-RPC over a Windows named pipe. The default pipe is `\\.\pipe\ember-lab-studio`. Studio takes the part after `ember-lab-` with `--lab-pipe NAME` (the bare name `studio`, or the full pipe name). Each request is one line on its own pipe connection and the reply is one line back. Nothing leaves the machine: the LOCAL · NO CLOUD chip says so.

## What Studio asks the lab

- `ping`: is the lab there. The Hour view's `ember-lab` check and the Train tab's "lab not answering" use it.
- Start a job (an hour or a learn job), ask a job's state, exit code and events, list jobs, stop a job. The Hour view, Console and Timeline use these.
- The Agent tab runs the lab's `agent` command as a child process and reads its output, one JSON object per line: the model's state (cold, waking, awake, asleep, yielded), tokens as they stream, a final answer, a busy-card notice, or an error.

Studio's own record of what it asked is its **press receipts**, a JSON-lines file written before each step, kept under `%LOCALAPPDATA%\ember-studio` unless `--press-receipts` says otherwise. The Timeline tab draws it.

## What happens when the lab is not there

Nothing breaks. Pages that need the lab say so in words, for example "the lab did not answer: the pipe does not exist, so the lab daemon is not running". A page that reads files (Library, Models, Weights) keeps working. `ember-studio status --lab-pipe <name of a pipe nobody serves>` prints the same sentence on the command line.

## The GPU card

One GPU is shared. The lab owns it: a job that trains or scores takes the card, and the resident model yields it while a job runs (the Agent tab shows YIELDED, and a message sent then gets a busy-card notice). Studio itself never touches the GPU, apart from reading its power and utilisation for the Train tab.

## What this build ships

This release ships Studio only. The lab daemon is built from the same commit but is not in the release: it still expects the author's machine layout (card lock folder, model server path and model locations are fixed paths), so it would not work on another computer yet. See [known limits](known-limits.md). Until the lab is released, Studio shows what it can read from files and says plainly when the lab is absent.
