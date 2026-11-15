# Platforms: what exists, what blocks the rest

Measured on 2026-11-15 against commit `185b8abd` of the private source repository.

## Windows (available)

Built on Windows 11 from a clean checkout of that commit, with the dependencies the lock file names, offline, four compile jobs at below-normal priority. The program's Windows subsystem is GUI (no console window). The exe was started with `ui-tree` and its output matched the build the documentation was written against, line for line apart from a timestamp.

## Linux (not available: it compiles, the tests do not)

**Result: no Linux download exists, and none will be published until the tests pass.** What was measured on 2026-11-15, in WSL (Ubuntu, Rust stable), from a `git archive` of the same committed tree:

- **Compiles.** The locked dependencies were fetched from crates.io at the versions and checksums in the lock file, and `cargo build --release --locked` finished in about two minutes with four jobs. No system package was needed to compile. The result is a 25 MB dynamically linked x86-64 ELF program. Disk used inside WSL: about 0.85 GB of build output and 0.58 GB of downloaded crates.
- **Draws.** `ui-tree` prints the control names, and `monitor --render-png` draws the Library, Models and Train tabs offscreen. A real window opened and drew the Agent tab under a virtual display (Xvfb). The windows were never shown on a desktop.
- **Says what it is.** The Train tab's context line reads `unsupported-platform` and its body reads `lab not answering`. The Agent tab, on first draw, showed `error: ember-lab agent state could not start: No such file or directory`, because no lab program exists there.
- **Tests do not build.** `cargo test --release --locked` stops with two compile errors: test code uses the Windows-only `std::os::windows` exit-status API. Until the test code is made portable and the tests pass, a Linux build is not released.
- **Not checked:** a Linux session with a real desktop (X11 or Wayland), mouse and keyboard use, the ember-cli panel, and the lab client on Linux. The program was never run against a lab.

What a complete Linux port still involves, read from the committed tree: 31 `cfg(windows)` sites in 13 source files and 15 `cfg(not(windows))` or `cfg(unix)` sites, mostly stubs. The lab client speaks a Windows named pipe, so it needs a Unix socket transport; the embedded ember-cli panel is a Windows pseudoconsole host; the single-window rule uses a Windows named mutex. These are why the platform line says `unsupported-platform`. A Linux Studio also needs a Linux ember-lab: the lab daemon has about 270 `cfg(windows)` sites (card lock, fixed paths, named pipe), and porting them is the larger half of the cure. It is queued after the folder settings; no date is promised.

**Next steps:** make the two test sites portable and run the tests; test the window on a real Linux desktop; add a Unix socket for the lab client; port the lab's Windows-only parts.

## macOS (not available)

**Result: no macOS build exists, and none can be built or tested from here (there is no Mac).**

What blocks it:

1. The same Windows-only parts as Linux (lab client pipe, ember-cli pseudoconsole host, single-window rule). The windowing stack (eframe with the glow renderer) supports macOS, so the user interface itself is not the blocker.
2. No NVIDIA GPU or NVML on a Mac. Studio's GPU readouts would be empty; the pages that do not need them are unaffected.
3. The lab daemon does not target macOS: it manages CUDA jobs, Windows job objects and card locks.
4. No hardware here, and no hosted runner that can read the private source for free.

What it would cost on GitHub-hosted runners. GitHub's published rules: standard runners are free on **public** repositories; on **private** repositories minutes are drawn from the account's monthly allowance, and one macOS minute counts as ten (Linux one, Windows two) ([GitHub: how use of Actions is measured](https://docs.github.com/en/billing/concepts/product-billing/github-actions)). The source is private, so a macOS build runs in a private repository and costs ten allowance minutes per minute. On a 2,000-minute allowance that is at most 200 macOS minutes a month. The account's actual allowance and usage could not be read: the billing endpoints need an extra token scope (`user`) that was not requested. No paid minutes were used or bought.

Cures, cheapest first:

- Do the port work (a Unix socket for the lab client, a pty for the cli panel) and test it on Linux first, where a build in WSL costs nothing.
- Build macOS on a Mac you own (a self-hosted runner or by hand) and attach the result to the release; nothing is billed.
- Run the macOS build on a hosted runner only for tagged releases, with caching, so a release costs a small number of the ten-times minutes.
- Publishing the source would make hosted macOS runners free, but that is the owner's decision and not part of this work.

## Summary

| OS | Today | First step |
| --- | --- | --- |
| Windows | build edb7d3ad, x64 | release it |
| Linux | none; compiles and draws in WSL, tests do not build | make the test code portable, then test on a real Linux desktop |
| macOS | none; no hardware, no free runner | port on Linux first, then build on a Mac |
