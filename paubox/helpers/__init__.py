"""
Send request builder and API error response handler.
"""

from .mail import Mail
from .errors import handle_error

# Re-exported for `from paubox.helpers import Mail, handle_error`. Declared here
# so linters do not report them as unused imports.
__all__ = ["Mail", "handle_error"]
