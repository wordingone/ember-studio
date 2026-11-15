# Install

> **Preview, Studio only.** This release contains Ember Studio and nothing else. Studio is a client of ember-lab and needs it to start or watch training, to run the Agent tab's model and to show live job state. **The ember-lab release is pending** until the lab's folders are configurable; no date is promised. Installing Studio alone gives you a window that opens and reads the folders you point it at, and says in words that the lab is not answering. It does not train or serve a model by itself.

## Which builds exist today

| OS | Build | Notes |
| --- | --- | --- |
| Windows 10/11, x64 | yes | `ember-studio-0.5.0-be2abf05-windows-x64.zip`, built from commit `be2abf05` of the private source repository on Windows 11 |
| Linux | no | It compiles and draws in WSL, but its tests do not build yet, so no download is published; see [platforms](platforms.md) |
| macOS | no | There is no Mac here to build or test on; what blocks it is in [platforms](platforms.md) |

Only Windows is supported today. Do not look for a Linux or macOS download: none exists.

## Windows

You need Windows 10 or 11 on 64-bit x86. There is no installer; Studio is one program you run from a folder.

1. Download `ember-studio-0.5.0-be2abf05-windows-x64.zip` and `SHA256SUMS` from the [Releases page](https://github.com/wordingone/ember-studio/releases).
2. Check the download. In PowerShell, in the folder you downloaded to:

   ```
   (Get-FileHash .\ember-studio-0.5.0-be2abf05-windows-x64.zip -Algorithm SHA256).Hash.ToLower()
   Get-Content .\SHA256SUMS
   ```

   The two hashes must be identical. If they are not, do not run the file.
3. Unzip it into a folder of your own, for example a `Programs\ember-studio` folder under your user profile. The zip holds `ember-studio-be2abf05.exe`, the release notes and `SHA256SUMS`. The name carries the short commit hash so you can tell builds apart.
4. Run `ember-studio-be2abf05.exe` (double-click it or run it from a terminal). A window titled "Ember Studio" opens. No console window opens with it.

**The build is not code-signed.** Windows SmartScreen may say "Windows protected your PC". The program is the one you checked against `SHA256SUMS`; choose More info, then Run anyway, only after that check.

### First launch

With nothing configured, Studio still opens. Pages that need a folder say which flag to give. To point them at your folders, start it from a terminal:

```
.\ember-studio-be2abf05.exe monitor --models-root D:\models --data-root D:\data --learn-root D:\learn-runs
```

All the roots are in [command line](command-line.md#roots-the-pages-read). Studio opens no network connection. The GPU readouts on Train use an NVIDIA driver; how the window behaves on a machine without one was not tested.

### Files Studio writes

By default Studio keeps its settings and its press receipts (a JSON-lines record of what it asked the lab to do) in `%LOCALAPPDATA%\ember-studio`. A research project file is saved where you tell it to be. To remove Studio, delete the folder you unzipped and, if you want, the `%LOCALAPPDATA%\ember-studio` folder.

### Update

Download the newer zip, check it, unzip it next to the old one. Settings carry over because they live in `%LOCALAPPDATA%`.

## Linux and macOS

Not available. See [platforms](platforms.md) for the state of each and what it would take.
