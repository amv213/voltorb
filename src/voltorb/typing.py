"""Custom type definitions."""

from enum import Enum, unique
from typing import NamedTuple


@unique
class EmissionFactorType(Enum):
    DIRECT = "direct"
    LIFECYCLE = "lifecycle"


@unique
class EstimationMethod(Enum):
    MEASURED = None
    CONSTRUCT_BREAKDOWN = "CONSTRUCT_BREAKDOWN"
    FORECASTS_HIERARCHY = "FORECASTS_HIERARCHY"
    MODE_BREAKDOWN = "MODE_BREAKDOWN"
    RECONSTRUCT_PRODUCTION_FROM_CONSUMPTION = "RECONSTRUCT_PRODUCTION_FROM_CONSUMPTION"
    THRESHOLD_FILTERED = "THRESHOLD_FILTERED"
    TIME_SLICER_AVERAGE = "TIME_SLICER_AVERAGE"


ZoneKey = str


class Coordinates(NamedTuple):
    longitude: float
    latitude: float


Geolocation = ZoneKey | Coordinates
