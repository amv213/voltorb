"""Authentication utilities."""

from collections.abc import Callable

import snug


def token_auth(auth_token: str) -> Callable[[snug.Request], snug.Request]:
    """Creates an HTTP header authentication callable.

    Params:
        auth_token: your Electricity Maps API token.

    Returns:
        A callable which adds header authentication to a :class:`Request`.
    """
    return snug.header_adder({"auth-token": auth_token})  # type: ignore[no-any-return]
