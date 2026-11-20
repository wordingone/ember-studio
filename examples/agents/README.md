# Agent examples

Two small Python scripts that drive `ember-studio` through commands the [command reference](../../docs/interface/commands.md) lists. Both read only: neither changes the window, starts a job or writes a file. They need Python 3 and nothing else.

| Script | What it does | Command it runs |
| --- | --- | --- |
| [`list_controls.py`](list_controls.py) | Prints every control of a tab with its role, name, value and whether it is disabled | `ember-studio ui-tree --json [--mode SLUG]` |
| [`check_job_start.py`](check_job_start.py) | Prints each preflight check for a job and exits 0 only when it could start | `ember-studio press ... --check --json` |

```
python examples/agents/list_controls.py path/to/ember-studio.exe --role Button
python examples/agents/check_job_start.py path/to/ember-studio.exe --script SCRIPT --sha256 HEX --log LOG
```

Both draw offscreen or ask the lab a question; they do not use `--act`, which changes a running window. Run `--act` only against a Studio you started for the purpose.
