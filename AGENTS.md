# AGENTS.md: read this before you change anything here

## 1. What this repository is and is not

This is the public face of Ember Studio: documentation, file formats and their schemas, job and experiment manifests, example agent scripts, themes, checks, and (once a release exists) the Releases page with the built programs and their checksums. It is **not** the program's source. A pull request that adds program source (Rust, a Cargo manifest, Python that is not a check or an example agent script) is closed with a pointer to this line. `python checks/allowlist.py` fails on such a path and names it.

## 2. What a contribution can be

A manual fix, a format example, a job kind or experiment manifest, an example experiment, an agent script, a theme, a check. Run the checks locally with one command:

```
python checks/run_all.py
```

What each failure means:

- `allowlist`: a path is not allowed here, is program source or a built program, names an internal package of the program, or holds a folder path of a build machine. Move or remove it.
- `docs`: a relative link or picture does not resolve, a picture is over 10 MB, or a text names a build-machine path or the private repository.
- `formats`: a schema is invalid, an example does not validate against its schema, or a schema accepts a deliberately broken copy.
- The `reds` steps prove each check fails on a broken tree. A check without its red is not finished.

## 3. The rule for examples

An example runs on a small open model, names the model and its licence, finishes in under ten minutes on a consumer card, and uses only commands the [command reference](docs/interface/commands.md) documents. An example agent script reads or operates the program only through those commands; no operating-system input, no UI Automation Invoke (Windows brings the target to the foreground for it).

## 4. The rule for docs

Every statement about the program must be true of the latest release, or say which build it was checked against. If you cannot check a statement against a release or the program's own documented behaviour, write that it was not checked. `docs/interface/` is generated from the program's source by its release process: do not edit it; open an issue to ask for a change. `docs/formats/` schemas are validated against their examples by `checks/validate_formats.py`.

## 5. Issues

Label a bug `bug`, a documentation mistake `docs`, a request `enhancement`. An acceptable bug report has: the build or release id, the steps, the receipt or log file the program wrote (remove anything private), and a picture of the window. The issue form asks for each.

## 6. Content rules

- No personal names in content, no secrets, no tokens, no links to private locations.
- No folder path of any machine (drive letters, user-profile paths, mount paths). Use `<folder>` placeholders and environment variables such as `%LOCALAPPDATA%`.
- No claims about speed or quality without the measurement and the build it came from.
- Say what does not work as plainly as what does.
