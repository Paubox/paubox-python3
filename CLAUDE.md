# CLAUDE.md — Paubox Python3 SDK

## Project Overview

Python3 SDK for Paubox APIs. Provides two independent clients:

- **`PauboxApiClient`** — HIPAA-compliant transactional email (requires API key)
- **`PauboxFormsClient`** — public form retrieval and submission (no auth required)

## Directory Structure

```
paubox/
  __init__.py       Public package exports: PauboxApiClient, PauboxFormsClient, Response
  paubox.py         PauboxApiClient + Response class
  forms.py          PauboxFormsClient (imports Response from paubox.py)
  helpers/
    __init__.py
    mail.py         Mail helper — formats email message dicts for the Email API
    errors.py       handle_error(error) — prints error response text and re-raises HTTPError

tests/
  test_paubox.py    Integration tests for the Email API (requires tests/config.cfg)
  test_forms.py     Unit tests for the Forms API (no credentials required)

setup.py            Package metadata and dependencies
README.md           User-facing documentation with code examples
api.md              Full API reference for both clients
CHANGELOG.md        Release history
```

## Running Tests

### Forms API unit tests (no credentials needed)

```bash
PYTHONPATH=. python tests/test_forms.py
```

### Email API integration tests

Requires `tests/config.cfg`:

```
PAUBOX_HOST: 'https://api.paubox.net/v1/YOUR_ENDPOINT_NAME'
PAUBOX_API_KEY: 'YOUR_API_KEY'
APPROVED_SENDER: 'sender@yourdomain.com'
```

```bash
PYTHONPATH=. python tests/test_paubox.py
```

## Key Design Decisions

- **`Response` class lives in `paubox/paubox.py`** and is imported by `forms.py` to avoid a breaking change. If you move it, update all importers.
- **`PauboxFormsClient` accepts an optional `base_url`** constructor argument for test injection (no real HTTP calls in unit tests).
- **Forms endpoints use `https://next.paubox.com`**; Email endpoints use a per-customer host set via `PAUBOX_HOST`.
- **No auth headers are sent for Forms API calls** — these are public endpoints called by form respondents.
- **`submit_form` validates `form_data` locally** before making the network call, raising `ValueError` if it is falsy (mirrors the API's 400 response).

## Environment Variables

| Variable | Used by | Description |
|---|---|---|
| `PAUBOX_API_KEY` | `PauboxApiClient` | Paubox Email API key |
| `PAUBOX_HOST` | `PauboxApiClient` | Email API base URL (e.g. `https://api.paubox.net/v1/your-endpoint`) |

`PauboxFormsClient` has no required environment variables; its base URL defaults to `https://next.paubox.com`.

## Adding a New API Surface

1. Create `paubox/<newapi>.py` with a new client class.
2. Import `Response` from `.paubox` (or from a future shared response module).
3. Use `handle_error` from `.helpers.errors` for consistent error handling.
4. Export the new class from `paubox/__init__.py`.
5. Add unit tests in `tests/test_<newapi>.py` using `unittest.mock.patch` — no live credentials.
6. Bump the minor version in `setup.py`, add an entry to `CHANGELOG.md`, and update `README.md` and `api.md`.
