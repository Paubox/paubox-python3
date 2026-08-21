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

## v1.0.1 / 2021-06-09

### 🎉 Enhancements

- [#3](https://github.com/Paubox/paubox-python3/pull/3) Add `requests` dependency to `setup.py`. ([@niwong](https://github.com/niwong))

## v1.0.0 / 2021-05-12

### 🚀 Major Release

This is the first release of the official Paubox-python3 package. This package is not intended to be backwards compatible with Python2, and users who are using Python2 should navigate to our Python2 [paubox-python](https://github.com/Paubox/paubox-python) package.

- [#1](https://github.com/Paubox/paubox-python3/pull/1) Build a working version of the Paubox-python3 SDK. ([@niwong](https://github.com/niwong))
