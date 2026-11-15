# Troubleshooting

Each entry is a sentence Studio really prints, or a behaviour observed on build `185b8abd`.

| You see | What it means and what to do |
| --- | --- |
| Starting Studio prints `STUDIO_ALREADY_RUNNING pid=<n>` and no new window opens | A Studio window already exists on this machine; there is only ever one. The second launch passed its arguments to it. Find the window by that process id or in the taskbar. Settings only a new window can take (for example `--lab-pipe`) are reported as ignored: close the open window first. |
| A page says `no models folder is configured: pass --models-root DIR or set EMBER_STUDIO_MODELS_ROOT` (or the same for data, learn, receipts, transplant runs, press receipts) | The page has no folder to read. Start Studio with that flag or set the variable. The flags are listed in [command line](command-line.md#roots-the-pages-read). |
| A page says `the lab did not answer: ... does not exist, so the lab daemon is not running` | Nothing serves the lab's named pipe. The lab daemon is not part of this release (see [known limits](known-limits.md)); pages that read files keep working. A pipe name given with `--lab-pipe` must be the part after `ember-lab-`. |
| The Train tab says `lab not answering` | The lab did not reply to Studio's ping. Same as above. |
| START HOUR is disabled and the text beside it names a reason | A check failed. Read the first row of **Before it starts** that is not OK. `?` blocks the same as NO. If the reason is "still running", an earlier job holds the lease: wait for it or stop it. |
| The Agent tab says Send is off | The text beside the button says why: no working folder yet, the box is empty, or a reply is streaming. |
| The Agent tab shows `COLD` | No model process is running; sending a message starts one. If a job holds the GPU card the chip shows `YIELDED` and a message gets a busy-card notice; send again when the job ends. |
| The ember-cli panel says `no program configured: give --cli-exe PATH or set EMBER_STUDIO_CLI_EXE` | The panel runs one program you name. Start Studio with `--cli-exe`. |
| A ribbon button is disabled | It carries the reason it is off. `ember-studio ui-tree --mode <tab>` prints it as the control's `.reason` read-out. |
| Console says `no row of this page is error lines (N rows read, all cut by the ribbon)` | ERRORS ONLY is on and the log has no error lines. Press it again to see the log. |
| Timeline says `no row of this page is the last hour` | The 1H range is on and nothing happened in the last hour. Press 24H or ALL. |
| `ember-studio --act NAME` does nothing | `NAME` must be a control name from `ui-tree` and a Studio window must be running. The command prints `STUDIO_ALREADY_RUNNING pid=<n>` when it handed the name to the window. |
| Windows says "Windows protected your PC" | The build is not code-signed. Verify the zip against `SHA256SUMS` first; see [install](install.md). |
| Studio is slow while a training job runs | Studio pins itself to two CPUs at below-normal priority on purpose so it never competes with a job. It is not stuck. |

If something here is wrong or missing, open an issue and include the build's short hash (it is in the exe's name) and the exact sentence on screen.
