# Changelog
All notable changes to this project will be documented in this file.

# v1.1.0 / 2026-05-21
### 🚀 New Features
- Add `PauboxFormsClient` with support for the Paubox Forms API (public endpoints, no API key required)
  - `get_form(form_id)` — retrieve form metadata, HTML, JSON schema, and CSS by UUID
  - `submit_form(form_id, form_data, attachments=None)` — submit form data with optional file attachments (up to 250 MB)
- Export `PauboxFormsClient` from the top-level `paubox` package
- Add unit tests for `PauboxFormsClient` (no live credentials required)
- Add `CLAUDE.md` project guide and `api.md` full API reference

# v1.0.0 / 2021-05-12
### 🚀 Major Release
This is the first release of the official Paubox-python3 package. This package is not intended to be backwards compatible with Python2, and users who are using Python2 should navigate to our Python2 [paubox-python](https://github.com/Paubox/paubox-python) package.

- [#1](https://github.com/Paubox/paubox-python3/pull/1) Build a working version of the Paubox-python3 SDK. ([@niwong](https://github.com/niwong))

# v1.0.1 / 2021-06-09
### 🎉 Enhancements
- [#3](https://github.com/Paubox/paubox-python3/pull/3) Add `requests` dependency to `setup.py`. ([@niwong](https://github.com/niwong))
