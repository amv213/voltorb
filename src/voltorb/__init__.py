"""Root of the package. The entire public API namespace is made available at this level."""

import logging

from ._patches import async_executor, execute, execute_async, executor
from ._version import __version__
from .api import Api as electricity_maps  # noqa: N813
from .auth import token_auth
from .exceptions import HTTPStatusError, UnauthorisedError, ValidationError
from .typing import Coordinates, EmissionFactorType, EstimationMethod, ZoneKey

__all__ = [
    "__version__",
    "electricity_maps",
    "token_auth",
    "execute",
    "HTTPStatusError",
    "ValidationError",
    "UnauthorisedError",
    "execute_async",
    "executor",
    "async_executor",
    "Coordinates",
    "ZoneKey",
    "EmissionFactorType",
    "EstimationMethod",
]


logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
