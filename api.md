# Paubox Python3 SDK — API Reference

## Overview

The SDK exposes two independent clients and a shared `Response` class:

| Class | Module | Auth required | Base URL |
|---|---|---|---|
| `PauboxApiClient` | `paubox.paubox` | Yes — `Token token=<key>` | Default `https://api.paubox.com/v1` (`PAUBOX_HOST` / `host` argument as optional override) |
| `PauboxFormsClient` | `paubox.forms` | Public endpoints: no. Management/export endpoints: yes — `Bearer <scoped api key>` | `https://api.paubox.com/forms` |
| `Response` | `paubox.paubox` | — | — |

All three are importable directly from the top-level package:

```python
import paubox
paubox.PauboxApiClient(...)
paubox.PauboxFormsClient(...)
# paubox.Response is returned by client methods, not instantiated directly
```

---

## `Response`

Wraps a `requests.Response` object returned by all client methods.

### Properties

| Property | Type | Description |
|---|---|---|
| `status_code` | `int` | HTTP status code |
| `headers` | `dict` | Response headers |
| `text` | `str` | Raw response body |
| `content` | `bytes` | Raw response body as bytes — use for binary responses (CSV/PDF exports) |
| `to_dict` | `dict` or `None` | Response body parsed as JSON; `None` if body is empty |

---

## Email API — `PauboxApiClient`

### Constructor

```python
PauboxApiClient(api_key=None, host=None)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `api_key` | `str` | `os.environ.get('PAUBOX_API_KEY')` | Paubox Email API key. No username/endpoint name is needed — the key alone authenticates. |
| `host` | `str` | `os.environ.get('PAUBOX_HOST')`, falling back to `https://api.paubox.com/v1` (`PAUBOX_API_BASE_URL`) | Optional override of the Email API base URL |

### `send(mail)`

Send a message through the Paubox Email API.

```
POST {host}/messages
Authorization: Token token={api_key}
```

**Parameters**

| Parameter | Type | Description |
|---|---|---|
| `mail` | `dict` | Formatted message dict. Use `Mail.get()` or build manually (see README). |

**Returns** `Response` — `status_code` 200 on success. `response.to_dict['sourceTrackingId']` contains the tracking ID.

**Raises** `requests.exceptions.HTTPError` on failure.

**Example**

```python
from paubox.helpers.mail import Mail
import paubox

client = paubox.PauboxApiClient("YOUR_API_KEY")
mail = Mail("sender@yourdomain.com", "Hello!", ["recipient@example.com"], {"text/plain": "Hi"})
response = client.send(mail.get())
tracking_id = response.to_dict["sourceTrackingId"]
```

### `get(tracking_code)`

Retrieve the delivery disposition of a sent message.

```
GET {host}/message_receipt?sourceTrackingId={tracking_code}
Authorization: Token token={api_key}
```

**Parameters**

| Parameter | Type | Description |
|---|---|---|
| `tracking_code` | `str` | `sourceTrackingId` returned from `send()` |

**Returns** `Response` — disposition data in `response.to_dict`.

**Raises** `requests.exceptions.HTTPError` on failure.

---

## Forms API — `PauboxFormsClient`

The Forms API has two kinds of endpoints:

- **Public endpoints** (`get_form`, `submit_form`) — no API key is required. They are intended to be called by form respondents (or on their behalf), and never send auth headers even when the client has an `api_key`.
- **Authenticated endpoints** (everything else) — require a **Paubox scoped API key** with the **`forms` scope**, sent as `Authorization: Bearer <api_key>`. JWTs are also accepted. Calling an authenticated method without an `api_key` raises `ValueError` before any network call.

### Constructor

```python
PauboxFormsClient(base_url="https://api.paubox.com/forms", api_key=None)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `base_url` | `str` | `"https://api.paubox.com/forms"` | Forms API base URL. Override for testing. |
| `api_key` | `str` or `None` | `None` | Paubox scoped API key with the `forms` scope (or a JWT). Required only for authenticated endpoints. |

### `get_form(form_id)`

Retrieve a form's full definition (metadata, HTML, JSON schema, CSS).

```
GET {base_url}/public/form_data/{form_id}
```

**Parameters**

| Parameter | Type | Description |
|---|---|---|
| `form_id` | `str` | UUID of the form to retrieve |

**Returns** `Response` — `status_code` 200. `response.to_dict` contains the form object:

| Field | Type | Description |
|---|---|---|
| `id` | `str` (UUID) | Form UUID |
| `title` | `str` | Form title |
| `description` | `str` or `null` | Optional description |
| `form_html` | `str` or `null` | Rendered HTML for embedding |
| `form_json` | `object` or `null` | JSON schema of form fields |
| `form_css` | `str` or `null` | CSS for the form |
| `active` | `bool` | Whether the form accepts submissions |
| `signable` | `bool` | Whether the form supports signatures |
| `submission_count` | `int` | Total submissions received |
| `customer_id` | `int` | Owning customer ID |
| `created_at` | `str` (ISO 8601) | Creation timestamp |
| `updated_at` | `str` (ISO 8601) | Last updated timestamp |

**Raises** `requests.exceptions.HTTPError` on 404 (form not found) or other HTTP errors.

**Example**

```python
import paubox

client = paubox.PauboxFormsClient()
response = client.get_form("550e8400-e29b-41d4-a716-446655440000")
form = response.to_dict
print(form["title"])     # "Patient Intake Form"
print(form["active"])    # True
```

### `submit_form(form_id, form_data, attachments=None)`

Submit a respondent's answers for a form. Maximum request size is **250 MB**.

```
POST {base_url}/api/forms/{form_id}/submissions
```

**Parameters**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `form_id` | `str` | Yes | UUID of the form being submitted |
| `form_data` | `dict` | Yes | Key-value pairs matching the form's field schema (`form_json`). Structure varies per form. |
| `attachments` | `list` or `None` | No | List of attachment dicts. Each must have `name` (filename) and `content` (base64-encoded bytes). |

**Returns** `Response` — `status_code` 201, empty body (`response.to_dict` is `None`).

**Raises**
- `ValueError` — if `form_data` is `None` or empty.
- `requests.exceptions.HTTPError` — on 400 (missing `form_data`) or 404 (form not found).

**Examples**

Text fields only:

```python
import paubox

client = paubox.PauboxFormsClient()
response = client.submit_form(
    "550e8400-e29b-41d4-a716-446655440000",
    form_data={"first_name": "Jane", "last_name": "Doe", "email": "jane@example.com"}
)
print(response.status_code)  # 201
```

With file attachments:

```python
import paubox
import base64

client = paubox.PauboxFormsClient()

with open("consent.pdf", "rb") as f:
    encoded = base64.b64encode(f.read()).decode("utf-8")

response = client.submit_form(
    "550e8400-e29b-41d4-a716-446655440000",
    form_data={"first_name": "Jane", "signature": "{signature_field}"},
    attachments=[{"name": "consent.pdf", "content": encoded}]
)
print(response.status_code)  # 201
```

### `list_forms(customer_id=None, form_id=None, search=None, order=None, order_by=None, archived=None, active=None, page=None, items=None)`

**Authenticated.** List forms visible to the API key, with filtering, ordering, and pagination.

```
GET {base_url}/api/forms
Authorization: Bearer {api_key}
```

**Parameters** (all optional; `None` values are omitted from the query string; booleans are serialized as lowercase `"true"`/`"false"`)

| Parameter | Type | Description |
|---|---|---|
| `customer_id` | `int` or `None` | Customer whose forms to list. Effectively required for API-key callers — the server returns 403 Forbidden when omitted. Pass the customer ID your key is scoped to (or a related customer's) |
| `form_id` | `str` or `None` | Filter to a single form UUID |
| `search` | `str` or `None` | Matches against form title and description |
| `order` | `str` or `None` | `"asc"` or `"desc"` (default `"desc"`) |
| `order_by` | `str` or `None` | One of `title`, `updated_at`, `submission_count`; anything else falls back to `created_at` |
| `archived` | `bool` or `None` | Filter by archived state |
| `active` | `bool` or `None` | Filter by active state |
| `page` | `int` or `None` | Page number (default 1) |
| `items` | `int` or `None` | Items per page (default 50, server caps at 100) |

**Returns** `Response` — `response.to_dict`:

| Field | Type | Description |
|---|---|---|
| `results` | `list` | List of form objects |
| `page_info` | `object` | `{"count", "pages", "page", "items"}` |

**Raises**
- `ValueError` — if the client has no `api_key`.
- `requests.exceptions.HTTPError` — on auth failure or other HTTP errors.

**Example**

```python
import paubox

client = paubox.PauboxFormsClient(api_key="YOUR_SCOPED_API_KEY")
response = client.list_forms(customer_id=12345, search="intake", order="asc", order_by="title", items=25)
for form in response.to_dict["results"]:
    print(form["title"])
```

### `get_form_by_id(form_id)`

**Authenticated.** Retrieve a single form — the authenticated variant of the public `get_form`.

```
GET {base_url}/api/forms/{form_id}
Authorization: Bearer {api_key}
```

**Parameters**

| Parameter | Type | Description |
|---|---|---|
| `form_id` | `str` | UUID of the form to retrieve |

**Returns** `Response` — `response.to_dict` is `{"data": {...form...}}`.

**Raises**
- `ValueError` — if the client has no `api_key`.
- `requests.exceptions.HTTPError` — on 404 (form not found) or other HTTP errors.

### `create_form(title, form_json, customer_id, description=None, form_html=None, form_css=None, recipient=None, signable=False, signature_confirmation_label=None, subscription_list_id=None, form_type=None, active=False, version=1, submission_count=0)`

**Authenticated.** Create a new form.

```
POST {base_url}/api/forms
Authorization: Bearer {api_key}
```

**Parameters** (optional parameters that are `None` are omitted from the JSON body)

| Parameter | Type | Required | Description |
|---|---|---|---|
| `title` | `str` | Yes | Form title |
| `form_json` | `dict` | Yes | Form definition (JSON schema of form fields) |
| `customer_id` | `int` | Yes | Owning customer ID |
| `description` | `str` or `None` | No | Form description |
| `form_html` | `str` or `None` | No | Rendered HTML for embedding |
| `form_css` | `str` or `None` | No | CSS for the form |
| `recipient` | `str` or `None` | No | Comma-separated string of notification email addresses |
| `signable` | `bool` | No | Whether the form supports signatures (default `False`) |
| `signature_confirmation_label` | `str` or `None` | No | Label for the signature confirmation checkbox |
| `subscription_list_id` | `str` or `None` | No | Subscription list to attach |
| `form_type` | `str` or `None` | No | Form type — sent as the JSON key `"type"` |
| `active` | `bool` | No | Whether the form accepts submissions (default `False`) |
| `version` | `int` | No | Form version (default `1`) |
| `submission_count` | `int` | No | Initial submission count (default `0`) |

**Returns** `Response` — `response.to_dict` is `{"id": "<new-uuid>"}`.

**Raises**
- `ValueError` — if the client has no `api_key`.
- `requests.exceptions.HTTPError` — on validation or other HTTP errors.

**Example**

```python
import paubox

client = paubox.PauboxFormsClient(api_key="YOUR_SCOPED_API_KEY")
response = client.create_form(
    title="Patient Intake Form",
    form_json={"fields": [{"name": "first_name", "type": "text"}]},
    customer_id=12345,
    recipient="intake@yourdomain.com",
    active=True
)
new_form_id = response.to_dict["id"]
```

### `update_form(form_id, title=None, description=None, form_json=None, vanity_url=None, recipient=None, active=None, subscription_list_id=None)`

**Authenticated.** Update a form. PATCH-style merge on the server: only keys present in the body are changed, so the SDK includes only the arguments that are not `None`.

```
PUT {base_url}/api/forms/{form_id}
Authorization: Bearer {api_key}
```

**Parameters**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `form_id` | `str` | Yes | UUID of the form to update |
| `title` | `str` or `None` | No | New title |
| `description` | `str` or `None` | No | New description |
| `form_json` | `dict` or `None` | No | New form definition |
| `vanity_url` | `str` or `None` | No | New vanity URL. Note: the server currently accepts this field but does not persist it — the value is silently ignored even though the call returns 200 |
| `recipient` | `str` or `None` | No | Comma-separated notification email addresses |
| `active` | `bool` or `None` | No | Activate/deactivate the form |
| `subscription_list_id` | `str` or `None` | No | Subscription list to attach |

**Returns** `Response` — `response.to_dict` is `{"detail": "Form updated successfully", "form_id": "<id>"}`.

**Raises**
- `ValueError` — if the client has no `api_key`.
- `requests.exceptions.HTTPError` — on 404 (form not found) or other HTTP errors.

### `archive_form(form_id)`

**Authenticated.** Archive a form (archiving also deactivates the form server-side).

```
POST {base_url}/api/forms/{form_id}/archive
Authorization: Bearer {api_key}
```

**Parameters**

| Parameter | Type | Description |
|---|---|---|
| `form_id` | `str` | UUID of the form to archive |

**Returns** `Response` — `response.to_dict` is `{"detail": "Form archived."}`.

**Raises**
- `ValueError` — if the client has no `api_key`.
- `requests.exceptions.HTTPError` — on 404 (form not found) or other HTTP errors.

### `unarchive_form(form_id)`

**Authenticated.** Unarchive a form.

```
POST {base_url}/api/forms/{form_id}/unarchive
Authorization: Bearer {api_key}
```

**Parameters**

| Parameter | Type | Description |
|---|---|---|
| `form_id` | `str` | UUID of the form to unarchive |

**Returns** `Response` — `response.to_dict` is `{"detail": "Form unarchived."}`.

**Raises**
- `ValueError` — if the client has no `api_key`.
- `requests.exceptions.HTTPError` — on 404 (form not found) or other HTTP errors.

### `copy_form(form_id, title)`

**Authenticated.** Copy an existing form under a new title.

```
POST {base_url}/api/forms/copy
Authorization: Bearer {api_key}
```

**Body** `{"form_id": "<source-uuid>", "title": "<new title>"}`

**Parameters**

| Parameter | Type | Description |
|---|---|---|
| `form_id` | `str` | UUID of the source form |
| `title` | `str` | Title for the copy |

**Returns** `Response` — `response.to_dict` is the full new form object (fresh UUID, `vanity_url` cleared, `submission_count` 0).

**Raises**
- `ValueError` — if the client has no `api_key`.
- `requests.exceptions.HTTPError` — on 404 (source form not found) or other HTTP errors.

### `get_form_stats(customer_id=None)`

**Authenticated.** Retrieve aggregate form statistics.

```
GET {base_url}/api/forms/stats
Authorization: Bearer {api_key}
```

**Parameters**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `customer_id` | `int` or `None` | No | Customer to report on (defaults server-side to the key's customer) |

**Returns** `Response` — `response.to_dict`:

| Field | Type | Description |
|---|---|---|
| `active_form_count` | `int` | Number of active forms |
| `total_submission_count` | `int` | Total submissions across all forms |
| `submissions_last_7_days` | `int` | Submissions received in the last 7 days |

**Raises**
- `ValueError` — if the client has no `api_key`.
- `requests.exceptions.HTTPError` — on auth failure or other HTTP errors.

### `list_submissions(form_id, submission_id=None, order_by=None, order=None, page=None, items=None)`

**Authenticated.** List a form's submissions, with ordering and pagination.

```
GET {base_url}/api/forms/{form_id}/submissions
Authorization: Bearer {api_key}
```

**Parameters** (`None` values are omitted from the query string)

| Parameter | Type | Required | Description |
|---|---|---|---|
| `form_id` | `str` | Yes | UUID of the form |
| `submission_id` | `str` or `None` | No | Filter to a single submission UUID |
| `order_by` | `str` or `None` | No | `submitter_email`; anything else falls back to `created_at` |
| `order` | `str` or `None` | No | `"asc"` or `"desc"` |
| `page` | `int` or `None` | No | Page number |
| `items` | `int` or `None` | No | Items per page (server caps at 100) |

**Returns** `Response` — `response.to_dict` is `{"data": [submission...], "total", "page", "items"}`. Each submission object:

| Field | Type | Description |
|---|---|---|
| `id` | `str` (UUID) | Submission UUID |
| `form_id` | `str` (UUID) | Parent form UUID |
| `form_data` | `str` | Submitted data as a JSON **string** — parse with `json.loads` |
| `storage_type` | `str` or `null` | Storage backend for the submission |
| `storage_url` | `str` or `null` | Storage location URL |
| `submitter_email` | `str` or `null` | Respondent's email address |
| `recipients` | `str` or `null` | Notification recipients |
| `attachment_name` | `str` or `null` | Attachment filename |
| `attachment_url` | `str` or `null` | Attachment URL |
| `attachment_type` | `str` or `null` | Attachment content type |
| `created_at` | `str` (ISO 8601) | Submission timestamp |

**Raises**
- `ValueError` — if the client has no `api_key`.
- `requests.exceptions.HTTPError` — on 404 (form not found) or other HTTP errors.

### `export_submissions_csv(form_id, submission_id=None)`

**Authenticated.** Export a form's submissions as CSV — all submissions, or a single one.

```
GET {base_url}/api/forms/{form_id}/submissions/submission-csv                    # all submissions
GET {base_url}/api/forms/{form_id}/submissions/submission-csv/{submission_id}    # single submission
Authorization: Bearer {api_key}
```

**Parameters**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `form_id` | `str` | Yes | UUID of the form |
| `submission_id` | `str` or `None` | No | Export a single submission instead of all |

**Returns** `Response` — CSV bytes (`text/csv`, attachment). Use `response.content` for the bytes.

**Raises**
- `ValueError` — if the client has no `api_key`.
- `requests.exceptions.HTTPError` — on 404 (form or submission not found) or other HTTP errors.

**Example**

```python
import paubox

client = paubox.PauboxFormsClient(api_key="YOUR_SCOPED_API_KEY")
response = client.export_submissions_csv("550e8400-e29b-41d4-a716-446655440000")
with open("submissions.csv", "wb") as f:
    f.write(response.content)
```

### `export_submission_pdf(form_id, submission_id)`

**Authenticated.** Export a single submission as a PDF.

```
GET {base_url}/api/forms/{form_id}/submissions/{submission_id}/submission-pdf
Authorization: Bearer {api_key}
```

**Parameters**

| Parameter | Type | Description |
|---|---|---|
| `form_id` | `str` | UUID of the form |
| `submission_id` | `str` | UUID of the submission |

**Returns** `Response` — PDF bytes (`application/pdf`). Use `response.content` for the bytes.

**Raises**
- `ValueError` — if the client has no `api_key`.
- `requests.exceptions.HTTPError` — on 404 (form or submission not found) or other HTTP errors.

**Example**

```python
import paubox

client = paubox.PauboxFormsClient(api_key="YOUR_SCOPED_API_KEY")
response = client.export_submission_pdf(
    "550e8400-e29b-41d4-a716-446655440000",
    "9b2d1c3e-4f5a-6789-abcd-ef0123456789"
)
with open("submission.pdf", "wb") as f:
    f.write(response.content)
```

---

## Error Handling

All client methods raise `requests.exceptions.HTTPError` on non-2xx responses. The `handle_error` helper (`paubox.helpers.errors`) prints the error response body to stdout before re-raising, which aids debugging.

```python
import requests
import paubox

client = paubox.PauboxFormsClient()
try:
    response = client.get_form("nonexistent-uuid")
except requests.exceptions.HTTPError as e:
    print(e.response.status_code)  # 404
```

`submit_form` additionally raises `ValueError` before any network call if `form_data` is falsy:

```python
try:
    client.submit_form("form-uuid", form_data=None)
except ValueError as e:
    print(e)  # "form_data is required and must not be empty"
```

Authenticated Forms methods likewise raise `ValueError` before any network call if the client was constructed without an `api_key`.

---

## Mail Helper — `Mail`

Convenience class for building Email API message dicts. Located in `paubox.helpers.mail`.

### Constructor

```python
Mail(from_, subject, recipients, content, optional_headers=None)
```

| Parameter | Type | Description |
|---|---|---|
| `from_` | `str` | Sender email address |
| `subject` | `str` | Email subject |
| `recipients` | `list[str]` | List of recipient email addresses |
| `content` | `dict` | `{"text/plain": "...", "text/html": "..."}`. HTML is auto-encoded to base64. |
| `optional_headers` | `dict` or `None` | See table below |

**Optional headers**

| Key | Type | Description |
|---|---|---|
| `reply_to` | `str` | Reply-to address |
| `bcc` | `str` or `list` | BCC recipient(s) |
| `cc` | `list[str]` | CC recipients |
| `attachments` | `list[dict]` | Each dict: `{"fileName": "...", "contentType": "...", "content": "<base64>"}` |
| `forceSecureNotification` | `bool` or `str` | Send as secure portal notification |
| `allowNonTLS` | `bool` | Allow delivery without TLS (non-PHI only) |

### `get()`

Returns the formatted message dict ready to pass to `PauboxApiClient.send()`.
