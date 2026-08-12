<img src="https://avatars.githubusercontent.com/u/22528478?s=200&v=4" alt="Paubox" width="150px">

# Paubox Python3 Package

**NEW:** [Version 2 of the Paubox Email API SDK for Python](https://github.com/Paubox/paubox-python3/tree/sdk-generation/v2.0.0-beta) is available to beta test now. It includes code for newer features like bulk message sending, dynamic templates, and more. We will be deprecating the old in the near future.

This is the official **Python3** package for the Paubox Email API. 

The Paubox Email API allows your application to send secure, HIPAA compliant email via [Paubox](https://www.paubox.com) and track email deliveries and opens.

# Table of Contents
*  [Installation](#installation)
*  [Usage](#usage)
   *  [Sending Email](#sending-messages-with-the-paubox-mail-helper)
   *  [Checking Email Dispositions](#checking-email-dispositions)
   *  [Paubox Forms API](#paubox-forms-api)
   *  [Paubox Forms — authenticated endpoints (scoped API keys)](#paubox-forms-authenticated)
*  [Contributing](#contributing)
*  [License](#license)

## External Resources
*  [Documentation](https://docs.paubox.com/email-api)
*  [Quickstart Guide](https://docs.paubox.com/email-api/quickstart)
*  [Changelog](https://github.com/Paubox/paubox-python3/blob/master/CHANGELOG.md)

<a name="#installation"></a>
## Installation

### Getting Paubox API Credentials
You will need to have a Paubox account. You can [sign up here](https://www.paubox.com/pricing/paubox-email-api).

Once you have an account, follow the instructions on the REST API dashboard to verify domain ownership and generate API keys. Further **[quickstart instructions for this process can be found here.](https://docs.paubox.com/email-api/quickstart)**

### Configuring API Credentials Locally

While you can simply hard-code your authentication credentials, it's often better practice to tuck these values away in an environment or configuration file. Our following code snippets leverage the use of the [`config`](https://docs.red-dove.com/cfg/python.html#python-getting-started) python package to load our credentials. To set `config` up, include your API key credentials in a config file (e.g. `config.cfg`)

```
PAUBOX_HOST: 'https://api.paubox.net/v1/YOUR_ENDPOINT_NAME'
PAUBOX_API_KEY: 'YOUR_API_KEY'
```

Then, install the `config` package using pip3 to load API credentials from the
`config.cfg` file:

```
$ pip3 install config
```

### Install Package
```
$ pip3 install paubox-python3
```

### Dependencies
[Requests](https://github.com/requests/requests)

<a name="#usage"></a>
## Usage

### Sending Messages with the Paubox Mail Helper

Sending via Paubox is easy. This is the minimum content needed to send an email.

```python
import paubox
from paubox.helpers.mail import Mail

from config import Config 
with open("config.cfg") as config_file:
    paubox_config = Config(config_file)

paubox_client = paubox.PauboxApiClient(paubox_config['PAUBOX_API_KEY'], paubox_config['PAUBOX_HOST'])
recipients = ["recipient@example.com"]
from_ = "sender@yourdomain.com"
subject = "Testing!"
content = {"text/plain": "Hello World!"}
mail = Mail(from_, subject, recipients, content)
response = paubox_client.send(mail.get())
print(response.status_code)
print(response.headers)
print(response.text)
```
### Sending Messages without the Mail Helper Class
```python
import paubox

from config import Config 
with open("config.cfg") as config_file:
    paubox_config = Config(config_file)

paubox_client = paubox.PauboxApiClient(paubox_config['PAUBOX_API_KEY'], paubox_config['PAUBOX_HOST'])
mail = {
    "data": {
        "message": {
            "recipients": [
                "recipient@example.com"
            ],
            "headers": {
                "subject": "Testing!",
                "from": "sender@yourdomain.com"
            },
            "content": {
                "text/plain": "Hello World!",
            }
        }
    }
}
response = paubox_client.send(mail)
print(response.status_code)
print(response.headers)
print(response.text)
```

### Allowing non-TLS message delivery

If you want to send non-PHI mail that does not need to be HIPAA compliant, you can allow the message delivery to take place even if a TLS connection is unavailable.

This means the message will not be converted into a secure portal message when a nonTLS connection is encountered. For this, just pass `allowNonTLS` as `True` as shown below:

#### Using Mail Class Helper
```python
import paubox
from paubox.helpers.mail import Mail

from config import Config 
with open("config.cfg") as config_file:
    paubox_config = Config(config_file)

paubox_client = paubox.PauboxApiClient(paubox_config['PAUBOX_API_KEY'], paubox_config.['PAUBOX_HOST'])
recipients = ["recipient@example.com"]
from_ = "sender@yourdomain.com"
subject = "Testing!"
content = {
    "text/plain": "Hello World!"    
}
optional_headers = {    
    'reply_to': 'replies@yourdomain.com',    
    'allowNonTLS': True
}
mail = Mail(from_, subject, recipients, content, optional_headers)
response = paubox_client.send(mail.get())
print(response.status_code)
print(response.headers)
print(response.text)
```

#### Without the Mail Class Helper
```python
import paubox

from config import Config 
with open("config.cfg") as config_file:
    paubox_config = Config(config_file)

paubox_client = paubox.PauboxApiClient(paubox_config['PAUBOX_API_KEY'], paubox_config['PAUBOX_HOST'])
mail = {
    "data": {
        "message": {
            "recipients": [
                "recipient@example.com"
            ],            
            'allowNonTLS': True,
            "headers": {
                "subject": "Testing!",
                "from": "Sender <sender@yourdomain.com>",
                "reply-to": "Reply-to <replies@yourdomain.com>"
            },
            "content": {
                "text/plain": "Hello World!",              
            }            
        }
    }
}
response = paubox_client.send(mail)
print(response.status_code)
print(response.headers)
print(response.text)
```

### Forcing Secure Notifications

Paubox Secure Notifications allow an extra layer of security, especially when coupled with an organization's requirement for message recipients to use 2-factor authentication to read messages (this setting is available to org administrators in the Paubox Admin Panel).

Instead of receiving an email with the message contents, the recipient will receive a notification email that they have a new message in Paubox.

To enable this, pass the `forceSecureNotification` header as `True` as shown below:

#### Using Mail Class Helper
```python
import paubox
from paubox.helpers.mail import Mail

from config import Config
with open("config.cfg") as config_file:
    paubox_config = Config(config_file)

paubox_client = paubox.PauboxApiClient(paubox_config['PAUBOX_API_KEY'], paubox_config['PAUBOX_HOST'])
recipients = ["recipient@example.com"]
from_ = "sender@yourdomain.com"
subject = "Testing!"
content = {
    "text/plain": "Hello World!"    
}
optional_headers = {    
    'reply_to': 'replies@yourdomain.com',    
    'forceSecureNotification': True
}
mail = Mail(from_, subject, recipients, content, optional_headers)
response = paubox_client.send(mail.get())
print(response.status_code)
print(response.headers)
print(response.text)
```
#### Without the Mail Class Helper
```python
import paubox

from config import Config
with open("config.cfg") as config_file:
    paubox_config = Config(config_file)

paubox_client = paubox.PauboxApiClient(paubox_config['PAUBOX_API_KEY'], paubox_config['PAUBOX_HOST'])
mail = {
    "data": {
        "message": {
            "recipients": [
                "recipient@example.com"
            ],                        
            'forceSecureNotification': 'true',
            "headers": {
                "subject": "Testing!",
                "from": "Sender <sender@yourdomain.com>",
                "reply-to": "Reply-to <replies@yourdomain.com>"
            },
            "content": {
                "text/plain": "Hello World!"             
            }            
        }
    }
}
response = paubox_client.send(mail)
print(response.status_code)
print(response.headers)
print(response.text)
```

### Sending Messages with all available headers

#### Using Mail Class Helper
```python
import paubox
import base64
from paubox.helpers.mail import Mail

from config import Config
with open("config.cfg") as config_file:
    paubox_config = Config(config_file)

paubox_client = paubox.PauboxApiClient(paubox_config['PAUBOX_API_KEY'], paubox_config['PAUBOX_HOST'])
recipients = ["recipient@example.com"]
from_ = "sender@yourdomain.com"
subject = "Testing!"
attachment_content = base64.b64encode(bytes("Hello World!", encoding="utf-8")).decode()
content = {
    "text/plain": "Hello World!",
    "text/html": "<html><body><h1>Hello World!</h1></body></html>"
}
optional_headers = {
    "attachments": [{
        "fileName": "the_file.txt",
        "contentType": "text/plain",
        "content": attachment_content
    }],
    'reply_to': 'replies@yourdomain.com',
    'bcc': 'recipient2@example.com',
    'cc':['recipientcc@example.com'],
    'forceSecureNotification': 'true',
    'allowNonTLS': True
}
mail = Mail(from_, subject, recipients, content, optional_headers)
response = paubox_client.send(mail.get())
print(response.status_code)
print(response.headers)
print(response.text)
```

#### Without the Mail Class Helper
```python
import paubox
import base64

from config import Config
with open("config.cfg") as config_file:
    paubox_config = Config(config_file)

paubox_client = paubox.PauboxApiClient(paubox_config['PAUBOX_API_KEY'], paubox_config['PAUBOX_HOST'])
attachment_content = base64.b64encode("Hello World!".encode('utf-8')).decode('utf-8')
mail = {
    "data": {
        "message": {
            "recipients": [
                "recipient@example.com"
            ],
            "bcc": ["recipient2@example.com"],
            'cc':['recipientcc@example.com'],
            'forceSecureNotification':'true',
            'allowNonTLS': True,
            "headers": {
                "subject": "Testing!",
                "from": "Sender <sender@yourdomain.com>",
                "reply-to": "Reply-to <replies@yourdomain.com>"
            },
            "content": {
                "text/plain": "Hello World!",
                "text/html": "<html><body><h1>Hello World!</h1></body></html>"
            },
            "attachments": [{
                    "fileName": "the_file.txt",
                    "contentType": "text/plain",
                    "content": attachment_content
            }]
        }
    }
}
response = paubox_client.send(mail)
print(response.status_code)
print(response.headers)
print(response.text)
```

### Checking Email Dispositions
The `SOURCE_TRACKING_ID` of a message is returned in the response.text of your send request. Use response.to_dict to access the response text as a dictionary.
```python
import paubox

from config import Config
with open("config.cfg") as config_file:
    paubox_config = Config(config_file)

paubox_client = paubox.PauboxApiClient(paubox_config['PAUBOX_API_KEY'], paubox_config['PAUBOX_HOST'])
disposition_response = paubox_client.get("SOURCE_TRACKING_ID")
print(disposition_response.status_code)
print(disposition_response.headers)
print(disposition_response.text)
```
<a name="#paubox-forms-api"></a>
## Paubox Forms API

The Paubox Forms API lets you retrieve form definitions and submit responses. These endpoints are **public** — no API key is required.

### Getting a Form

Retrieve a form's metadata, HTML, JSON schema, and CSS by its UUID.

```python
import paubox

forms_client = paubox.PauboxFormsClient()
response = forms_client.get_form("your-form-uuid-here")
print(response.status_code)   # 200
print(response.to_dict)       # dict with id, title, form_html, form_json, form_css, etc.
```

### Submitting a Form

```python
import paubox

forms_client = paubox.PauboxFormsClient()
response = forms_client.submit_form(
    "your-form-uuid-here",
    form_data={"first_name": "Jane", "last_name": "Doe", "email": "jane@example.com"}
)
print(response.status_code)   # 201
```

### Submitting a Form with File Attachments

Attachments must be base64-encoded. Maximum total request size is 250 MB.

```python
import paubox
import base64

forms_client = paubox.PauboxFormsClient()

with open("consent.pdf", "rb") as f:
    encoded = base64.b64encode(f.read()).decode("utf-8")

response = forms_client.submit_form(
    "your-form-uuid-here",
    form_data={"first_name": "Jane", "signature": "{signature_field}"},
    attachments=[{"name": "consent.pdf", "content": encoded}]
)
print(response.status_code)   # 201
```

<a name="#paubox-forms-authenticated"></a>
## Paubox Forms — authenticated endpoints (scoped API keys)

Beyond the public endpoints above, `PauboxFormsClient` can manage forms and retrieve/export submissions. These endpoints require authentication:

*  Pass a **Paubox scoped API key** carrying the **`forms` scope** as the `api_key` constructor argument. The key is sent as a Bearer token (`Authorization: Bearer <key>`) on every authenticated call. JWTs are also accepted.
*  The public endpoints (`get_form`, `submit_form`) never send auth headers, even when `api_key` is set.
*  Calling an authenticated method without an `api_key` raises `ValueError` before any network call.

```python
import paubox

forms_client = paubox.PauboxFormsClient(api_key="YOUR_SCOPED_API_KEY")
```

### Managing Forms

```python
import paubox

forms_client = paubox.PauboxFormsClient(api_key="YOUR_SCOPED_API_KEY")

# List forms (paginated; pass the customer_id your key is scoped to —
# API-key calls that omit it are rejected with 403 Forbidden)
response = forms_client.list_forms(customer_id=12345, search="intake", order="asc", order_by="title", page=1, items=25)
print(response.to_dict["results"])      # list of forms
print(response.to_dict["page_info"])    # {"count", "pages", "page", "items"}

# Get a single form (authenticated variant of get_form)
response = forms_client.get_form_by_id("your-form-uuid-here")
print(response.to_dict["data"])

# Create a form
response = forms_client.create_form(
    title="Patient Intake Form",
    form_json={"fields": [{"name": "first_name", "type": "text"}]},
    customer_id=12345,
    description="New patient intake",
    recipient="intake@yourdomain.com,frontdesk@yourdomain.com",
    active=True
)
print(response.to_dict["id"])           # UUID of the new form

# Update a form — only the arguments you pass are changed
response = forms_client.update_form("your-form-uuid-here", title="Updated Title", active=False)
print(response.to_dict["detail"])       # "Form updated successfully"

# Archive / unarchive (archiving also deactivates the form)
forms_client.archive_form("your-form-uuid-here")
forms_client.unarchive_form("your-form-uuid-here")

# Copy a form
response = forms_client.copy_form("your-form-uuid-here", "Copy of Patient Intake Form")
print(response.to_dict["id"])           # UUID of the copy

# Form stats
response = forms_client.get_form_stats()
print(response.to_dict)                 # {"active_form_count", "total_submission_count", "submissions_last_7_days"}
```

### Retrieving and Exporting Submissions

```python
import paubox

forms_client = paubox.PauboxFormsClient(api_key="YOUR_SCOPED_API_KEY")

# List a form's submissions (paginated)
response = forms_client.list_submissions("your-form-uuid-here", page=1, items=50)
for submission in response.to_dict["data"]:
    print(submission["id"], submission["submitter_email"])
    print(submission["form_data"])      # JSON string — parse with json.loads if needed

# Export all submissions as CSV
response = forms_client.export_submissions_csv("your-form-uuid-here")
with open("submissions.csv", "wb") as f:
    f.write(response.content)

# Export a single submission as CSV
response = forms_client.export_submissions_csv("your-form-uuid-here", "submission-uuid-here")
with open("submission.csv", "wb") as f:
    f.write(response.content)

# Export a single submission as PDF
response = forms_client.export_submission_pdf("your-form-uuid-here", "submission-uuid-here")
with open("submission.pdf", "wb") as f:
    f.write(response.content)
```

<a name="#contributing"></a>
## Contributing
The Paubox-python3 SDK is maintained by [Paubox, Inc.](https://www.paubox.com)

We want to empower our users building applications with the Paubox Email API, and so we encourage you to file bug reports/create GitHub issues and pull requests. Chances are other developers using our Email API might be having similar ideas about new features or approaches to improving the SDK, so we encourage you to upvote or comment on existing issues or pull requests! 

<a name="#license"></a>
## License

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## Copyright
Copyright &copy; 2021, Paubox, Inc.
## 💬 Community & support

Questions, ideas, or want to share what you built? Join the **[Paubox Community](https://github.com/Paubox/community/discussions)** — the single home for discussions across every Paubox SDK and API.

🔐 Found a security issue? Email **devops@paubox.com** — please don't post it publicly.
