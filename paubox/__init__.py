"""
This library allows you to send emails through the Paubox Transactional Email
API application and get the email disposition of sent emails.
"""

from .paubox import PauboxApiClient, Response
from .forms import PauboxFormsClient
NAME = "paubox"

# Public package surface. Declared so linters do not report the re-exports above
# as unused imports.
__all__ = ["PauboxApiClient", "PauboxFormsClient", "Response", "NAME"]
