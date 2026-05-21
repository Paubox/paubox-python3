# Paubox Python3 SDK — API Reference

## Overview

The SDK exposes two independent clients and a shared `Response` class:

| Class | Module | Auth required | Base URL |
|---|---|---|---|
| `PauboxApiClient` | `paubox.paubox` | Yes — `Token token=<key>` | Per-customer (`PAUBOX_HOST`) |
| `PauboxFormsClient` | `paubox.forms` | No | `https://apx.paubox.com/forms` |
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
| `to_dict` | `dict` or `None` | Response body parsed as JSON; `None` if body is empty |

---

## Email API — `PauboxApiClient`

### Constructor

```python
PauboxApiClient(api_key=None, host=None)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `api_key` | `str` | `os.environ.get('PAUBOX_API_KEY')` | Paubox Email API key |
| `host` | `str` | `os.environ.get('PAUBOX_HOST')` | Email API base URL |

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

client = paubox.PauboxApiClient("YOUR_API_KEY", "https://api.paubox.net/v1/YOUR_ENDPOINT")
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

These are **public endpoints** — no API key is required. They are intended to be called by form respondents (or on their behalf).

### Constructor

```python
PauboxFormsClient(base_url="https://apx.paubox.com/forms")
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `base_url` | `str` | `"https://apx.paubox.com/forms"` | Forms API base URL. Override for testing. |

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
