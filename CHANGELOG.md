# Changelog

All notable changes to this project will be documented in this file.

## Unreleased

None of the work below has been published to PyPI. It previously sat under
`1.1.0`, `1.2.0`, and `1.3.0` headings, but those were `setup.py` bumps that
were never uploaded and never tagged — the newest release on PyPI is still
`1.0.1` from 2021-06-09. The three sections are merged here because they will
ship together as a single release.

### 🚀 New Features

- Add `PauboxFormsClient` with support for the Paubox Forms API (public endpoints, no API key required)
  - `get_form(form_id)` — retrieve form metadata, HTML, JSON schema, and CSS by UUID
  - `submit_form(form_id, form_data, attachments=None)` — submit form data with optional file attachments (up to 250 MB)
- Export `PauboxFormsClient` from the top-level `paubox` package
- Add authenticated Paubox Forms endpoints to `PauboxFormsClient` (scoped API keys with the `forms` scope, sent as `Authorization: Bearer <key>`; JWTs also accepted)
  - `PauboxFormsClient(base_url, api_key=None)` — new optional `api_key` constructor argument (backward compatible)
  - Form management: `list_forms(...)`, `get_form_by_id(form_id)`, `create_form(...)`, `update_form(...)`, `archive_form(form_id)`, `unarchive_form(form_id)`, `copy_form(form_id, title)`, `get_form_stats(customer_id=None)`
  - Submissions: `list_submissions(...)`, `export_submissions_csv(form_id, submission_id=None)`, `export_submission_pdf(form_id, submission_id)`
  - Existing public endpoints (`get_form`, `submit_form`) still send no auth headers
- Add `Response.content` property exposing the raw response bytes (for CSV/PDF exports)
- A username (per-customer endpoint name) is no longer required to authenticate the Paubox APIs — an API key alone is enough
- `PauboxApiClient` `host` is now optional and defaults to `https://api.paubox.com/v1`, so `PauboxApiClient("YOUR_API_KEY")` works with no host configured. The `PAUBOX_HOST` environment variable and the `host` constructor argument are still honored as overrides (backward compatible)
- Forms base URL moved from `https://apx.paubox.com/forms` to `https://api.paubox.com/forms`

### 🎉 Enhancements

- Remove the `http://localhost` fallback in `PauboxApiClient.send()` — the client now always uses the configured host (or the new default)
- Add unit tests for `PauboxFormsClient` and all authenticated methods (no live credentials required)
- Add `CLAUDE.md` project guide and `api.md` full API reference

### 🔒 Hardening

- Validate every caller-supplied value interpolated into a request URL path. A `form_id` or `submission_id` containing `..`, `/`, `?` or `#` would otherwise change which endpoint is called: `requests` resolves dot-segments while preparing a URL, so the retargeting happens client-side, and a rewritten path can leave the `/forms` base path on the same host and carry the `Authorization` header with it.
  - Authenticated endpoints raise `ValueError` unless the id is a UUID.
  - `get_form` and `submit_form` percent-encode the id rather than rejecting it, so any id they accepted before still works. The bare dot-segments `.` and `..` are rejected, because encoding cannot neutralize them — `quote()` leaves `.` alone and `requests` un-escapes `%2E` during preparation.
- No published release was affected: the newest version on PyPI predates `PauboxFormsClient` entirely.

## [1.1.0](https://github.com/Paubox/paubox-python3/compare/v1.0.1...v1.1.0) (2026-08-21)


### Features

* add authenticated Forms API support via scoped API keys ([111750a](https://github.com/Paubox/paubox-python3/commit/111750a07904c06de86bc95832aa34a9f7c51e31))
* add authenticated Forms API support via scoped API keys ([87af1bf](https://github.com/Paubox/paubox-python3/commit/87af1bfb1dd60077105c3401496888cf947ff06b))


### Bug Fixes

* validate path segments in PauboxFormsClient URLs ([c392a69](https://github.com/Paubox/paubox-python3/commit/c392a69381e1bd44ecb1cb5889aa9b04e47f38d2))
* validate path segments in PauboxFormsClient URLs ([1877d75](https://github.com/Paubox/paubox-python3/commit/1877d7591fa209ea1c9523a0b8f9fc5c693ee118))


### Documentation

* link Paubox Community discussions ([ec70f90](https://github.com/Paubox/paubox-python3/commit/ec70f90fe5d3d3b3cd7d48148421b1c0a52415e6))
* update paubox.com/paubox.net links to current URLs ([13e6a03](https://github.com/Paubox/paubox-python3/commit/13e6a0352294f73fc4d30213cf65efde052aaa57))
* update paubox.com/paubox.net links to current URLs ([cec9e40](https://github.com/Paubox/paubox-python3/commit/cec9e400bdc7291529840a277473f5705d8db6d3))

## v1.0.1 / 2021-06-09

### 🎉 Enhancements

- [#3](https://github.com/Paubox/paubox-python3/pull/3) Add `requests` dependency to `setup.py`. ([@niwong](https://github.com/niwong))

## v1.0.0 / 2021-05-12

### 🚀 Major Release

This is the first release of the official Paubox-python3 package. This package is not intended to be backwards compatible with Python2, and users who are using Python2 should navigate to our Python2 [paubox-python](https://github.com/Paubox/paubox-python) package.

- [#1](https://github.com/Paubox/paubox-python3/pull/1) Build a working version of the Paubox-python3 SDK. ([@niwong](https://github.com/niwong))
