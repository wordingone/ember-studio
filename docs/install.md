# Install

> **Preview. No release has been published yet**, so there is nothing to download today; this page says how installing will work. Studio is a client of ember-lab and needs a lab to start or watch training, to run the Agent tab's resident model and to show live job state. Installing Studio alone gives you a window that opens and reads the folders you point it at, and says in words that the lab is not answering. It does not train or serve a model by itself. The lab is built from the same source but has not been released either; see [lab](lab.md).

## Which builds exist

| OS | Build | Notes |
| --- | --- | --- |
| Windows 10/11, x64 | the documentation was checked against build `de6494fe` (version 0.5.0) | A release will be a zip named `ember-studio-<release tag>-windows-x64.zip` on the [Releases page](https://github.com/wordingone/ember-studio/releases), with a checksum file beside it |
| Linux | no | It compiled and drew in WSL when last measured, on an earlier build, and its tests did not build; see [platforms](platforms.md) |
| macOS | no | There is no Mac here to build or test on; what blocks it is in [platforms](platforms.md) |

Only Windows is supported today. Do not look for a Linux or macOS download: none exists.

## Windows

You need Windows 10 or 11 on 64-bit x86. There is no installer; Studio is one program you run from a folder.

1. Download the zip and the checksum file (`SHA256SUMS.txt`) from the Releases page, once a release exists.
2. Check the download. In PowerShell, in the folder you downloaded to, with the zip's real name:

   ```
   (Get-FileHash .\ember-studio-<release tag>-windows-x64.zip -Algorithm SHA256).Hash.ToLower()
   Get-Content .\SHA256SUMS.txt
   ```

   The two hashes must be identical. If they are not, do not run the file.
3. Unzip it into a folder of your own, for example a `Programs\ember-studio` folder under your user profile. The release workflow in this repository packs `ember-studio.exe`, the README and the licence.
4. Run `ember-studio.exe` (double-click it or run it from a terminal). A window titled "Ember Studio" opens, on the Agent tab. No console window opens with it.

**The build is not code-signed.** Windows SmartScreen may say "Windows protected your PC". The program is the one you checked against the checksum file; choose More info, then Run anyway, only after that check.

### First launch

With nothing configured, Studio still opens. Pages that need a folder say which flag to give. To point them at your folders, start it from a terminal:

```
.\ember-studio.exe monitor --models-root <models folder> --data-root <data folder> --learn-root <learn folder>
```

All the roots are in [command line](command-line.md#roots-the-pages-read). The Agent tab needs a working folder (BROWSE, or type it) and a model: the lab's resident model, or one you name in a provider config file ([Agent](tabs/agent.md#choosing-the-model)). Studio opens no network connection of its own. The GPU readouts on Train use an NVIDIA driver; how the window behaves on a machine without one was not tested.

### Files Studio writes

Studio keeps these in `%LOCALAPPDATA%\ember-studio` unless a flag or variable says otherwise:

- `settings.json`: the Agent tab's working folder and a few window choices (dock, panels). `EMBER_STUDIO_SETTINGS` names another file.
- `last-tab.txt`: the tab you were on.
- `press-receipts.jsonl`: a JSON-lines record of what it asked the lab to do (`--press-receipts`).
- `agent-sessions`: your saved Agent sessions (`EMBER_STUDIO_AGENT_SESSIONS` names another folder).

A research project file is saved where you tell it to be. To remove Studio, delete the folder you unzipped and, if you want, the `%LOCALAPPDATA%\ember-studio` folder.

### Update

Download the newer zip, check it, unzip it next to the old one. Settings carry over because they live in `%LOCALAPPDATA%`.

## Linux and macOS

Not available. See [platforms](platforms.md) for the state of each and what it would take.
