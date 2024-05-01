"""Custom exception classes.

Our exception hierarchy:

* HTTPError
  x HTTPStatusError
    - UnauthorisedError
* ValidationError
"""

from typing import Any

import snug


class HTTPError(Exception):
    """Base class for all network related errors."""


class HTTPStatusError(HTTPError):
    """The response had an error HTTP status code of 4xx or 5xx"""

    def __init__(
        self, message: str, *, response: snug.Response, request: snug.Request
    ) -> None:
        self.request = request
        self.response = response
        super().__init__(message)


class UnauthorisedError(HTTPStatusError):
    """The response had a 401 HTTP status code."""


class ValidationError(Exception):
    """Raised on failed deserialisation of the API response."""

    def __init__(self, *, response: snug.Response, response_schema: Any) -> None:
        self.response = response
        message = f"Error deserialising response into '{response_schema!r}'"
        super().__init__(message)
