"""Common middlewares, decorators, and other higher-oder functions for handling request / response API interactions."""

import json
from collections.abc import Callable
from functools import partial
from typing import ParamSpec, TypeVar

import cattrs
import snug
from gentools import compose, map_return, relay, reusable

from voltorb._patches import Query
from voltorb.exceptions import (
    HTTPStatusError,
    UnauthorisedError,
    ValidationError,
)
from voltorb.serde import converter

P = ParamSpec("P")
T = TypeVar("T")


_CUSTOM_HEADERS = {"content-type": "application/json", "user-agent": "voltorb/0.1.0"}


def _raise_for_status(response: snug.Response, request: snug.Request) -> None:
    """Raises on HTTP status errors, if any occurred.

    Raises:
        :class:`HTTPStatusError`: on a response with a HTTP status error.
        :class:`UnauthorisedError`: on a response with a 401 Unauthorized HTTP status errors.
    """

    if response.status_code < 400:  # noqa: PLR2004
        return

    message = f"Response with status code {response.status_code} for URL {request.url!r}: {json.loads(response.content)}"

    # raise custom error on 401 UNAUTHORIZED
    # might be useful for users to be able to discriminate
    if response.status_code == 401:  # noqa: PLR2004
        raise UnauthorisedError(message, response=response, request=request)

    # else raise basic error wrapper
    raise HTTPStatusError(message, response=response, request=request)


def request_preparation_middleware(request: snug.Request) -> Query[snug.Response]:
    """Performs common 'preparation' of requests relayed through the middleware."""
    response = yield request.with_headers(_CUSTOM_HEADERS)
    return response


def error_handling_middleware(request: snug.Request) -> Query[snug.Response]:
    """Performs error handling on request / responses relayed through the middleware."""

    response = yield request

    _raise_for_status(response, request=request)

    return response


def deserialiser(response: snug.Response, response_schema: type[T]) -> T:
    """Deserialises a response into the given schema."""
    response_payload = json.loads(response.content)

    try:
        return converter.structure(response_payload, cl=response_schema)
    except cattrs.BaseValidationError as e:
        raise ValidationError(response=response, response_schema=response_schema) from e


def rest_query(
    *, response_schema: type[T]
) -> Callable[[Callable[P, Query[snug.Response]]], Callable[P, Query[T]]]:
    """Decorator that instruments generic API interactions by relaying requests through shared middleware,
    and returning the response as a deserialised model.

    References:
        https://snug.readthedocs.io/en/latest/advanced.html#composing-queries
    """

    return compose(  # type: ignore[no-any-return]
        # START
        # -> Generator[snug.Request, snug.Response, snug.Response]
        reusable,  # convenience function to make query reusable
        # -> Iterator[Generator[snug.Request, snug.Response, snug.Response]]
        relay(request_preparation_middleware, error_handling_middleware),
        #       YIELDED snug.Request -> first middleware -> second middleware -> ...
        #       RETURN snug.Response <- first middleware <- second middleware <- ... <- SEND snug.Response
        # -> Iterator[Generator[snug.Request, snug.Response, snug.Response]]
        map_return(partial(deserialiser, response_schema=response_schema)),
        # -> Iterator[Generator[snug.Request, snug.Response, T]]
        # END
    )
