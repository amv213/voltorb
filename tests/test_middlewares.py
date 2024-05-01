import pytest
import snug
from attrs import frozen

from voltorb import execute
from voltorb.exceptions import (
    HTTPStatusError,
    UnauthorisedError,
    ValidationError,
)
from voltorb.middlewares import rest_query


@frozen
class ExpectedResponseSchema:
    a: int
    b: int


@rest_query(response_schema=ExpectedResponseSchema)
def mock_endpoint_get():
    return (yield snug.Request("GET", "https://mock/url"))


def test_middleware_decorated_query_is_reusable(fixture_mock_client):
    """That the middleware makes the query reusable."""
    query = mock_endpoint_get()

    mock_response = snug.Response(200, content=b'{"a": 1, "b": 2}')
    client = fixture_mock_client(mock_response, mock_response)

    assert execute(query, client=client)
    assert execute(query, client=client)


def test_middleware_decorated_query_adds_custom_headers(fixture_mock_client):
    """That the middleware adds expected custom headers."""
    query = mock_endpoint_get()

    mock_response = snug.Response(200, content=b'{"a": 1, "b": 2}')
    client = fixture_mock_client(mock_response)

    execute(query, client=client)
    request_sent = client.request

    assert request_sent.headers.get("content-type") == "application/json"
    assert "user-agent" in request_sent.headers


def test_middleware_decorated_query_raises_for_status_on_http_error(
    fixture_mock_client,
):
    """That the middleware raises HTTPStatusErrors if receiving HTTP error status codes."""
    query = mock_endpoint_get()

    mock_response = snug.Response(500, content=b'{"message": "error"}')
    client = fixture_mock_client(mock_response)

    with pytest.raises(HTTPStatusError):
        execute(query, client=client)


def test_middleware_decorated_query_raises_on_unauthorised_status_code(
    fixture_mock_client,
):
    """That the middleware raises an UnauthorisedError if receiving q 401 HTTP error response."""
    query = mock_endpoint_get()

    mock_response = snug.Response(401, content=b'{"message": "invalid token"}')
    client = fixture_mock_client(mock_response)

    with pytest.raises(UnauthorisedError):
        execute(query, client=client)


@pytest.mark.parametrize(
    "response_content",
    [
        b'{"a": 1, "b": 2}',
        b'{"a": 1, "b": 2, "c": 3}',
    ],
    ids=[
        "exact-match",
        # should try to be flexible to server-side non-breaking API changes
        "with-extras",
    ],
)
def test_middleware_decorated_query_deserialises_response_into_response_schema(
    fixture_mock_client, response_content
):
    """That the middleware deserialises responses into expected schema."""
    query = mock_endpoint_get()

    mock_response = snug.Response(200, content=response_content)
    client = fixture_mock_client(mock_response)

    returned = execute(query, client=client)
    assert isinstance(returned, ExpectedResponseSchema)


def test_middleware_decorated_query_raises_validation_error_on_validation_errors(
    fixture_mock_client,
):
    """That the middleware raises a ValidationError if failing to deserialise response into schema."""
    query = mock_endpoint_get()

    mock_response = snug.Response(200, content=b'{"a": 1}')
    client = fixture_mock_client(mock_response)

    with pytest.raises(ValidationError):
        execute(query, client=client)
