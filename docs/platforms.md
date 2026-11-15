# Platforms: what exists, what blocks the rest

Measured on 2026-11-15 against commit `185b8abd` of the private source repository.

## Windows (available)

Built on Windows 11 from a clean checkout of that commit, with the dependencies the lock file names, offline, four compile jobs at below-normal priority. The program's Windows subsystem is GUI (no console window). The exe was started with `ui-tree` and its output matched the build the documentation was written against, line for line apart from a timestamp.

## Linux (not available)

**Result: no Linux build exists.** The attempt was made in WSL (Ubuntu, Rust 1.96, gcc present) from the same commit, using only a `git archive` of the committed tree. It stopped at dependency resolution: the Linux-only crates the lock file names (the Linux windowing and accessibility crates, for example `accesskit_unix`) are not in any local cache, and fetching them needs the network. No dependency was downloaded to make this attempt.

What this tells us about the code, read from the committed tree:

- The Windows-only parts of Studio are 31 `cfg(windows)` sites in 13 source files. Fifteen `cfg(not(windows))` or `cfg(unix)` sites already exist, mostly as stubs (single-instance, process handling, the home time zone, the press receipts path).
- The things a Linux build must still replace: the lab client is a Windows named-pipe client (`\\.\pipe\ember-lab-NAME`), so it needs a Unix socket transport; the embedded ember-cli panel is a Windows pseudoconsole (ConPTY) host, so it needs a pty (`openpty`) host; the single-window rule uses a Windows named mutex and pipe; the folder dialog of the Research project uses the Windows shell; GPU power and utilisation read NVML, which is present on Linux with an NVIDIA driver.
- The CI file already in this repository lists Linux GUI packages (libxkbcommon, GTK 3 and several libxcb development packages). They would be needed to build on Ubuntu.

**Cure and cost.** The smallest honest target is a Studio that runs on Linux as a viewer of files (Library, Models, Evals, Weights, Research, Timeline) with the lab client on a Unix socket. The five replacements above are each a bounded change; they are an estimate, not a measurement, and the lab daemon itself (about 270 `cfg(windows)` sites) is a much larger port and is not part of this target.

## macOS (not available)

**Result: no macOS build exists, and none can be built or tested from here (there is no Mac).**

What blocks it:

1. The same five Windows-only parts as Linux. The windowing stack (eframe with the glow renderer) supports macOS, so the user interface itself is not the blocker.
2. No NVIDIA GPU or NVML on a Mac. Studio's GPU readouts would be empty; the pages that do not need them are unaffected.
3. The lab daemon does not target macOS: it manages CUDA jobs, Windows job objects and card locks.
4. No hardware here, and no hosted runner that can read the private source for free.

What it would cost on GitHub-hosted runners. GitHub's published rules: standard runners are free on **public** repositories; on **private** repositories minutes are drawn from the account's monthly allowance, and one macOS minute counts as ten (Linux one, Windows two) ([GitHub: how use of Actions is measured](https://docs.github.com/en/billing/concepts/product-billing/github-actions)). The source is private, so a macOS build runs in a private repository and costs ten allowance minutes per minute. On a 2,000-minute allowance that is at most 200 macOS minutes a month. The account's actual allowance and usage could not be read: the billing endpoints need an extra token scope (`user`) that was not requested. No paid minutes were used or bought.

Cures, cheapest first:

- Do the port work (the five replacements) and test it on Linux first, where a build in WSL costs nothing.
- Build macOS on a Mac you own (a self-hosted runner or by hand) and attach the result to the release; nothing is billed.
- Run the macOS build on a hosted runner only for tagged releases, with caching, so a release costs a small number of the ten-times minutes.
- Publishing the source would make hosted macOS runners free, but that is the owner's decision and not part of this work.

## Summary

| OS | Today | First step |
| --- | --- | --- |
| Windows | build 185b8abd, x64 | release it |
| Linux | none; blocked on a dependency fetch, then the five replacements | fetch the locked crates in WSL and see how far the build gets |
| macOS | none; no hardware, no free runner | port on Linux first, then build on a Mac |
