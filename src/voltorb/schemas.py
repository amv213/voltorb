"""Datastructures and schema definitions for API responses."""

from datetime import datetime
from typing import TypeAlias

from attrs import frozen

from voltorb.serde import register_structure_hook, to_camel_case, to_whitespaced
from voltorb.typing import EmissionFactorType, EstimationMethod, ZoneKey

Datetime: TypeAlias = datetime


@register_structure_hook(alias_generator=to_camel_case)
@frozen
class ZoneMetadata:
    zone_name: str
    display_name: str | None = None
    country_name: str | None = None
    access: list[str] | None = None


Zones = dict[ZoneKey, ZoneMetadata]


@frozen
class Health:
    @frozen
    class MonitorHealth:
        state: str

    monitors: MonitorHealth
    status: str


@register_structure_hook(alias_generator=to_camel_case)
@frozen
class CarbonIntensity:
    zone: ZoneKey
    carbon_intensity: int
    datetime: Datetime
    updated_at: Datetime
    created_at: Datetime
    emission_factor_type: EmissionFactorType
    is_estimated: bool
    estimation_method: EstimationMethod


@frozen
class CarbonIntensityHistory:
    zone: ZoneKey
    history: list[CarbonIntensity]


@frozen
class CarbonIntensityRange:
    zone: ZoneKey
    data: list[CarbonIntensity]


@register_structure_hook(alias_generator=to_camel_case)
@frozen
class CarbonIntensityForecast:
    @register_structure_hook(alias_generator=to_camel_case)
    @frozen
    class Forecast:
        carbon_intensity: int
        datetime: Datetime

    zone: ZoneKey
    forecast: list[Forecast]
    updated_at: Datetime


@register_structure_hook(alias_generator=to_whitespaced)
@frozen
class PowerMix:
    biomass: int | None
    coal: int | None
    gas: int | None
    geothermal: int | None
    hydro: int | None
    nuclear: int | None
    solar: int | None
    oil: int | None
    wind: int | None
    unknown: int | None

    hydro_discharge: int | None
    battery_discharge: int | None


@register_structure_hook(alias_generator=to_camel_case)
@frozen
class PowerBreakdown:
    zone: ZoneKey
    datetime: Datetime
    updated_at: Datetime
    created_at: Datetime

    power_consumption_breakdown: PowerMix
    power_production_breakdown: PowerMix
    power_import_breakdown: dict[str, int]
    power_export_breakdown: dict[str, int]

    fossil_free_percentage: int | None
    renewable_percentage: int | None

    power_consumption_total: int | None
    power_production_total: int | None
    power_import_total: int | None
    power_export_total: int | None

    is_estimated: bool
    estimation_method: EstimationMethod


@frozen
class PowerBreakdownHistory:
    zone: ZoneKey
    history: list[PowerBreakdown]


@frozen
class PowerBreakdownRange:
    zone: ZoneKey
    data: list[PowerBreakdown]


@frozen
class PowerBreakdownForecast:
    zone: ZoneKey
    data: list[PowerBreakdown]


@register_structure_hook(alias_generator=to_camel_case)
@frozen
class PowerProductionBreakdownForecast:
    @register_structure_hook(alias_generator=to_camel_case)
    @frozen
    class Forecast:
        datetime: Datetime
        power_production_total: int
        power_production_breakdown: PowerMix

    zone: ZoneKey
    forecast: list[Forecast]
    updated_at: Datetime


@register_structure_hook(alias_generator=to_camel_case)
@frozen
class PowerConsumptionBreakdownForecast:
    @register_structure_hook(alias_generator=to_camel_case)
    @frozen
    class Forecast:
        datetime: Datetime
        power_consumption_total: int
        power_consumption_breakdown: PowerMix

    zone: ZoneKey
    forecast: list[Forecast]
    updated_at: Datetime


@register_structure_hook(alias_generator=to_camel_case)
@frozen
class Updates:
    @register_structure_hook(alias_generator=to_camel_case)
    @frozen
    class Update:
        datetime: Datetime
        updated_at: Datetime

    zone: ZoneKey
    updates: list[Update]
    threshold: str
    limit: int
    limit_reached: bool
