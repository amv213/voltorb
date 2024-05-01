import snug

from voltorb import token_auth


def test_token_auth_adds_token_to_auth_header():
    """That token authentication adds api tokens as request headers and under the expected key."""
    mock_auth_token = "API-TOKEN"  # noqa: S105
    authentication_method = token_auth(auth_token=mock_auth_token)
    request = snug.Request("GET", url="https://mock/url")

    authenticated_request = authentication_method(request)
    assert isinstance(authenticated_request, snug.Request)

    electricity_maps_auth_header_name = "auth-token"
    assert (
        authenticated_request.headers.get(electricity_maps_auth_header_name)
        == mock_auth_token
    )
