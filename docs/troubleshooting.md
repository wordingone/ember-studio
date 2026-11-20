# Troubleshooting

Each entry is a sentence Studio really prints or a behaviour read from the source of build `de6494fe`; entries that were observed in a window say so, and those were observed on the earlier build `185b8abd`.

| You see | What it means and what to do |
| --- | --- |
| Starting Studio prints `STUDIO_ALREADY_RUNNING pid=<n>` and no new window opens | A Studio window already exists on this machine; there is only ever one. The second launch passed its arguments to it. Find the window by that process id or in the taskbar. Settings only a new window can take (for example `--lab-pipe`) are reported as ignored: close the open window first. |
| A page says `no models folder is configured: pass --models-root DIR or set EMBER_STUDIO_MODELS_ROOT` (or the same for data, learn, receipts, transplant runs, press receipts) | The page has no folder to read. Start Studio with that flag or set the variable. The flags are listed in [command line](command-line.md#roots-the-pages-read). |
| A page says `the lab did not answer: ... does not exist, so the lab daemon is not running` | Nothing serves the lab's pipe. No lab has been released (see [known limits](known-limits.md)), so anything that needs one does not work until you run it. A pipe name given with `--lab-pipe` must be the part after `ember-lab-`. |
| A mode tab (Train, Console, Timeline or Agent) is drawn greyed and a click does nothing | The lab you are talking to does not serve what that tab needs, and the hover text says which verb is missing. Start a lab that does, or use the tabs that read your folders. From the source and a unit test; not seen in a live window. |
| The Train tab says `lab not answering` | The lab did not reply to Studio's ping. Same as above. |
| START HOUR is disabled and the text beside it names a reason | A check failed. Read the first row of **Before it starts** that is not OK. `?` blocks the same as NO. If the reason is "still running", an earlier job holds the lease: wait for it or stop it. |
| The Agent tab says Send is off | The text beside the button says why: no working folder yet, the box is empty, or a reply is streaming. |
| The Agent tab names a model it cannot use, or the lab's `capabilities` shows the Agent tab off with a sentence | The `model` key of your provider config file names a model the lab cannot serve: the provider id or the model id is not in the file, the model has `tool_call: false`, a `{env:NAME}` variable is not set, a `{file:...}` file is missing, or the address starts `https://` (only plain `http://` is supported: point the file at a local OpenAI-compatible server or proxy). The sentence names which. See [Agent](tabs/agent.md#choosing-the-model). |
| The state line says `compacting: ...` and the answer has not started | The session grew near the context's limit and the model is writing a summary of it; the conversation continues from that summary. See [Agent](tabs/agent.md#long-sessions-compaction). |
| A turn ends with `cut: ...` | The lab stopped it and says why, for example the thinking budget was reached or the answer hit the token limit. Send again, or raise the limit in the server file or the model's `limit.output`. See [Agent](tabs/agent.md#when-a-turn-is-cut). |
| A message you sent while a job held the card is shown `queued` (AUTO-REVIEW) or `not sent: card busy` (the other modes) | AUTO-REVIEW keeps the message and sends it when the card is free; a queued message has a Delete control. The other modes do not queue: send it again. |
| Lab commands refuse a custody argument | The custody drive is a setting with no built-in value. Name it in `ember-lab.toml` (`[custody] drive`) or `EMBER_CUSTODY_DRIVE`; `ember-lab paths` prints every setting and where its value came from. See [lab](lab.md). |
| The Agent tab shows `COLD` | No model process is running; sending a message starts one. If a job holds the GPU card the chip shows `YIELDED` and a message gets a busy-card notice; send again when the job ends. |
| The ember-cli panel says `no program configured: give --cli-exe PATH or set EMBER_STUDIO_CLI_EXE` | The panel runs one program you name. Start Studio with `--cli-exe`. |
| A ribbon button is disabled | It carries the reason it is off. `ember-studio ui-tree --mode <tab>` prints it as the control's `.reason` read-out. |
| Console says `no row of this page is error lines (N rows read, all cut by the ribbon)` | ERRORS ONLY is on and the log has no error lines. Press it again to see the log. |
| Timeline says `no row of this page is the last hour` | The 1H range is on and nothing happened in the last hour. Press 24H or ALL. |
| `ember-studio --act NAME` does nothing | `NAME` must be a control name from `ui-tree` and a Studio window must be running. The command prints `STUDIO_ALREADY_RUNNING pid=<n>` when it handed the name to the window. |
| Windows says "Windows protected your PC" | The build is not code-signed. Verify the zip against the checksum file first; see [install](install.md). |
| Studio is slow while a training job runs | Studio pins itself to two CPUs at below-normal priority on purpose so it never competes with a job. It is not stuck. `--cpu-mask` or `EMBER_STUDIO_CPU_MASK` changes the pin. |

If something here is wrong or missing, open an issue and include the build's short hash (Help, About names the version; the hash is in the release's file name once a release exists) and the exact sentence on screen.
