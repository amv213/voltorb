"""
Tests ensuring desired API objects are part of the top-level namespace (to help catch breaking changes)
"""

import pytest

import voltorb


def test_exports_version():
    """That the package exposes the __version__ variable."""
    assert hasattr(voltorb, "__version__")


@pytest.mark.parametrize(
    "name",
    [
        "electricity_maps",
        "token_auth",
        "HTTPStatusError",
        "ValidationError",
        "UnauthorisedError",
        "execute",
        "execute_async",
        "executor",
        "async_executor",
        "Coordinates",
        "ZoneKey",
        "EmissionFactorType",
        "EstimationMethod",
    ],
)
def test_is_in_root_package_namespace(name):
    """That the package exposes the given name."""
    assert hasattr(voltorb, name)
