# Security

This repository holds documents, formats, manifests, examples and checks. The program itself (Ember Studio and ember-lab) is built from a private repository and, once released, is published as files on the [Releases page](https://github.com/wordingone/ember-studio/releases).

## Reporting a problem

- For a vulnerability in a released program, use GitHub's private vulnerability reporting on this repository's Security tab if it is offered. If it is not, open an issue that says only that you have a security report and asks for a private channel. **Do not put exploit details, files from a victim's machine or secrets in a public issue.**
- For a mistake in this repository that leaks something (a secret, a personal name, a folder path of a machine), open an issue naming the file and line, without repeating the leaked text.

## What to expect

Reports are read by a maintainer and answered in the same place. No response time is promised. A confirmed problem in a release is fixed in a new release and named in the [changelog](CHANGELOG.md).

## Supported versions

No release has been published yet, so there is no supported version. When one exists, this page will say which releases receive fixes.

## Verifying a download

Every release will list a SHA-256 checksum file. Check the download against it before you run it ([install](docs/install.md)). The program is not code-signed yet, so Windows SmartScreen may warn.
