"""Electricity Maps API queries."""

from datetime import datetime, timezone

import snug
from typing_extensions import assert_never

from voltorb import schemas
from voltorb._patches import Query
from voltorb.middlewares import rest_query
from voltorb.typing import Coordinates, EmissionFactorType, Geolocation, ZoneKey

_API_PREFIX = "https://api.electricitymap.org"


def _as_utc_isoformat(dt: datetime) -> str:
    """Converts a datetime object to a UTC ISO 8601 format string."""
    is_naive = dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None
    if is_naive:
        dt = dt.replace(tzinfo=timezone.utc)

    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _geolocation_to_params(geolocation: Geolocation) -> dict[str, str | float]:
    """Converts a geolocation into corresponding query parameters."""
    match geolocation:
        case ZoneKey():
            return {"zone": geolocation}
        case Coordinates():
            return {"lon": geolocation.longitude, "lat": geolocation.latitude}
        case _ as unreachable:
            assert_never(unreachable)


def get_health() -> Query[snug.Response]:
    """This endpoint can be used to automatically verify that the Electricity Maps API is up."""
    request = snug.Request("GET", f"{_API_PREFIX}/health")
    return (yield request)


# using class structure of queries for simple namespacing
class Api:
    @staticmethod
    @rest_query(response_schema=schemas.Zones)
    def get_zones() -> Query[snug.Response]:
        """This endpoint returns all zones available if no auth-token is provided.

        If an auth-token is provided, it returns a list of zones and routes available with this token.
        """
        request = snug.Request("GET", f"{_API_PREFIX}/v3/zones")
        return (yield request)

    @staticmethod
    @rest_query(response_schema=schemas.Health)
    def get_health() -> Query[snug.Response]:
        """This endpoint can be used to automatically verify that the Electricity Maps API is up."""
        request = snug.Request("GET", f"{_API_PREFIX}/health")
        return (yield request)

    class carbon_intensity:
        @staticmethod
        @rest_query(response_schema=schemas.CarbonIntensity)
        def get_latest(
            geolocation: Geolocation,
            emission_factor_type: EmissionFactorType | None = None,
            disable_estimations: bool | None = None,
        ) -> Query[snug.Response]:
            """This endpoint retrieves the last known carbon intensity (in gCO2eq/kWh) of electricity consumed in an area.

            Args:
                geolocation: The geolocation for which to get data.
                emission_factor_type (optional): The emission factor type.
                disable_estimations (optional): Whether estimated data should be disabled.
            """
            request = snug.Request("GET", f"{_API_PREFIX}/v3/carbon-intensity/latest")

            params = _geolocation_to_params(geolocation)
            if emission_factor_type is not None:
                params.update(emissionFactorType=emission_factor_type.value)
            if disable_estimations is not None:
                params.update(disableEstimations=disable_estimations)

            return (yield request.with_params(params))

        @staticmethod
        @rest_query(response_schema=schemas.CarbonIntensityHistory)
        def get_history(
            geolocation: Geolocation,
            emission_factor_type: EmissionFactorType | None = None,
            disable_estimations: bool | None = None,
        ) -> Query[snug.Response]:
            """This endpoint retrieves the last 24 hours of carbon intensity (in gCO2eq/kWh) of an area.

            The resolution is 60 minutes.

            Args:
                geolocation: The geolocation for which to get data.
                emission_factor_type (optional): The emission factor type.
                disable_estimations (optional): Whether estimated data should be disabled.
            """
            request = snug.Request("GET", f"{_API_PREFIX}/v3/carbon-intensity/history")

            params = _geolocation_to_params(geolocation)
            if emission_factor_type is not None:
                params.update(emissionFactorType=emission_factor_type.value)
            if disable_estimations is not None:
                params.update(disableEstimations=disable_estimations)

            return (yield request.with_params(params))

        # TODO(avianello): requires commercial auth
        @staticmethod
        @rest_query(response_schema=schemas.CarbonIntensity)
        def get_past(
            geolocation: Geolocation,
            date_time: datetime,
            emission_factor_type: EmissionFactorType | None = None,
            disable_estimations: bool | None = None,
        ) -> Query[snug.Response]:
            """This endpoint retrieves a past carbon intensity (in gCO2eq/kWh) of an area.

            The resolution is 60 minutes.

            Args:
                geolocation: The geolocation for which to get data.
                date_time: The datetime for which to get data.
                emission_factor_type (optional): The emission factor type.
                disable_estimations (optional): Whether estimated data should be disabled.
            """
            request = snug.Request("GET", f"{_API_PREFIX}/v3/carbon-intensity/past")

            params = _geolocation_to_params(geolocation)
            params.update(datetime=_as_utc_isoformat(date_time))
            if emission_factor_type is not None:
                params.update(emissionFactorType=emission_factor_type.value)
            if disable_estimations is not None:
                params.update(disableEstimations=disable_estimations)

            return (yield request.with_params(params))

        # TODO(avianello): requires commercial auth
        @staticmethod
        @rest_query(response_schema=schemas.CarbonIntensityRange)
        def get_past_range(
            geolocation: Geolocation,
            start: datetime,
            end: datetime,
            disable_estimations: bool | None = None,
        ) -> Query[snug.Response]:
            """This endpoint retrieves a past carbon intensity (in gCO2eq/kWh) of an area within a given date range.

            The resolution is 60 minutes. The time range is limited to 10 days.

            Args:
                geolocation: The geolocation for which to get data.
                start: The start datetime for which to get data.
                end: The end datetime for which to get data (excluded).
                disable_estimations (optional): Whether estimated data should be disabled.
            """
            request = snug.Request(
                "GET", f"{_API_PREFIX}/v3/carbon-intensity/past-range"
            )

            params = _geolocation_to_params(geolocation)
            params.update(start=_as_utc_isoformat(start), end=_as_utc_isoformat(end))
            if disable_estimations is not None:
                params.update(disableEstimations=disable_estimations)

            return (yield request.with_params(params))

        # TODO(avianello): requires commercial auth
        @staticmethod
        @rest_query(response_schema=schemas.CarbonIntensityForecast)
        def get_forecast(geolocation: Geolocation) -> Query[snug.Response]:
            """This endpoint retrieves the forecasted carbon intensity (in gCO2eq/kWh) of an area.

            The endpoint returns 24 hours of forecasts. The forecasts span from horizon 0, which is the start of the current
            hour, to horizon 23. Ex: if the date and time is currently 2024-03-02 13:12:39 GMT, then the forecasts will cover
            the range from 2024-03-02 13:00:00 GMT to 2024-03-03 12:00:00 GMT.

            Args:
                geolocation: The geolocation for which to get data.
            """
            request = snug.Request("GET", f"{_API_PREFIX}/v3/carbon-intensity/forecast")

            params = _geolocation_to_params(geolocation)

            return (yield request.with_params(params))

    class marginal_carbon_intensity:
        # TODO(avianello): requires commercial auth
        @staticmethod
        @rest_query(response_schema=schemas.CarbonIntensity)
        def get_past(
            geolocation: Geolocation,
            date_time: datetime,
            disable_estimations: bool | None = None,
        ) -> Query[snug.Response]:
            """This endpoint retrieves a past marginal carbon intensity (in gCO2eq/kWh) of an area.

            The resolution is 60 minutes. The delay with the latest available data is between 1 and 2 months.

            Args:
                geolocation: The geolocation for which to get data.
                date_time: The datetime for which to get data.
                disable_estimations (optional): Whether estimated data should be disabled.
            """
            request = snug.Request(
                "GET", f"{_API_PREFIX}/v3/marginal-carbon-intensity/past"
            )

            params = _geolocation_to_params(geolocation)
            params.update(datetime=_as_utc_isoformat(date_time))
            if disable_estimations is not None:
                params.update(disableEstimations=disable_estimations)

            return (yield request.with_params(params))

        # TODO(avianello): requires commercial auth
        @staticmethod
        @rest_query(response_schema=schemas.CarbonIntensityRange)
        def get_past_range(
            geolocation: Geolocation,
            start: datetime,
            end: datetime,
            disable_estimations: bool | None = None,
        ) -> Query[snug.Response]:
            """This endpoint retrieves a past marginal carbon intensity (in gCO2eq/kWh) of an area within a given date range.

            The resolution is 60 minutes. The time range is limited to 10 days. The delay with the latest available data is
            between 1 and 2 months.

            Args:
                geolocation: The geolocation for which to get data.
                start: The start datetime for which to get data.
                end: The end datetime for which to get data (excluded).
                disable_estimations (optional): Whether estimated data should be disabled.
            """
            request = snug.Request(
                "GET", f"{_API_PREFIX}/v3/marginal-carbon-intensity/past-range"
            )

            params = _geolocation_to_params(geolocation)
            params.update(start=_as_utc_isoformat(start), end=_as_utc_isoformat(end))
            if disable_estimations is not None:
                params.update(disableEstimations=disable_estimations)

            return (yield request.with_params(params))

    class power_breakdown:
        @staticmethod
        @rest_query(response_schema=schemas.PowerBreakdown)
        def get_latest(
            geolocation: Geolocation, disable_estimations: bool | None = None
        ) -> Query[snug.Response]:
            """This endpoint retrieves the last known data about the origin of electricity in an area.

            "powerProduction" (in MW) represents the electricity produced in the zone, broken down by production type
            "powerConsumption" (in MW) represents the electricity consumed in the zone, after taking into account imports and exports, and broken down by production type.
            "powerExport" and "Power import" (in MW) represent the physical electricity flows at the zone border
            "renewablePercentage" and "fossilFreePercentage" refers to the % of the power consumption breakdown coming from renewables or fossil-free power plants (renewables and nuclear)

            Args:
                geolocation: The geolocation for which to get data.
                disable_estimations (optional): Whether estimated data should be disabled.
            """
            request = snug.Request("GET", f"{_API_PREFIX}/v3/power-breakdown/latest")

            params = _geolocation_to_params(geolocation)
            if disable_estimations is not None:
                params.update(disableEstimations=disable_estimations)

            return (yield request.with_params(params))

        @staticmethod
        @rest_query(response_schema=schemas.PowerBreakdownHistory)
        def get_history(
            geolocation: Geolocation, disable_estimations: bool | None = None
        ) -> Query[snug.Response]:
            """This endpoint retrieves the last 24 hours of power consumption and production breakdown of an area,
            which represents the physical origin of electricity broken down by production type.

            The resolution is 60 minutes.

            Args:
                geolocation: The geolocation for which to get data.
                disable_estimations (optional): Whether estimated data should be disabled.
            """
            request = snug.Request("GET", f"{_API_PREFIX}/v3/power-breakdown/history")

            params = _geolocation_to_params(geolocation)
            if disable_estimations is not None:
                params.update(disableEstimations=disable_estimations)

            return (yield request.with_params(params))

        # TODO(avianello): requires commercial auth
        @staticmethod
        @rest_query(response_schema=schemas.PowerBreakdown)
        def get_past(
            geolocation: Geolocation,
            date_time: datetime,
            disable_estimations: bool | None = None,
        ) -> Query[snug.Response]:
            """This endpoint retrieves a past power breakdown of an area.

            The resolution is 60 minutes.

            Args:
                geolocation: The geolocation for which to get data.
                date_time: The datetime for which to get data.
                disable_estimations (optional): Whether estimated data should be disabled.
            """
            request = snug.Request("GET", f"{_API_PREFIX}/v3/power-breakdown/past")

            params = _geolocation_to_params(geolocation)
            params.update(datetime=_as_utc_isoformat(date_time))
            if disable_estimations is not None:
                params.update(disableEstimations=disable_estimations)

            return (yield request.with_params(params))

        # TODO(avianello): requires commercial auth
        @staticmethod
        @rest_query(response_schema=schemas.PowerBreakdownRange)
        def get_past_range(
            geolocation: Geolocation,
            start: datetime,
            end: datetime,
            disable_estimations: bool | None = None,
        ) -> Query[snug.Response]:
            """This endpoint retrieves a past power breakdown of an area within a given date range.

            The resolution is 60 minutes. The time range is limited to 10 days.

            Args:
                geolocation: The geolocation for which to get data.
                start: The start datetime for which to get data.
                end: The end datetime for which to get data (excluded).
                disable_estimations (optional): Whether estimated data should be disabled.
            """
            request = snug.Request(
                "GET", f"{_API_PREFIX}/v3/power-breakdown/past-range"
            )

            params = _geolocation_to_params(geolocation)
            params.update(start=_as_utc_isoformat(start), end=_as_utc_isoformat(end))
            if disable_estimations is not None:
                params.update(disableEstimations=disable_estimations)

            return (yield request.with_params(params))

        # TODO(avianello): requires commercial auth
        @staticmethod
        @rest_query(response_schema=schemas.PowerBreakdownForecast)
        def get_forecast(geolocation: Geolocation) -> Query[snug.Response]:
            """This endpoint retrieves the most recent forecasted data about the origin of electricity in an area.

            Note that for some zones, only the power production, or power consumption breakdown is available.
            Forecasts of imports and exports are unavailable at the moment.

            The endpoint returns 24 hours of forecasts. The forecasts span from horizon 0, which is the start of the current
            hour, to horizon 23. Ex: if the date and time is currently 2024-03-02 13:12:39 GMT, then the forecasts will cover
            the range from 2024-03-02 13:00:00 GMT to 2024-03-03 12:00:00 GMT.

            Args:
                geolocation: The geolocation for which to get data.
            """
            request = snug.Request("GET", f"{_API_PREFIX}/v3/power-breakdown/forecast")

            params = _geolocation_to_params(geolocation)

            return (yield request.with_params(params))

    class power_production_breakdown:
        # TODO(avianello): requires commercial auth
        @staticmethod
        @rest_query(response_schema=schemas.PowerProductionBreakdownForecast)
        def get_forecast(geolocation: Geolocation) -> Query[snug.Response]:
            """This endpoint retrieves the forecasted power production breakdown of an area by production type.

            The endpoint returns 24 hours of forecasts. The forecasts span from horizon 0, which is the start of the current
            hour, to horizon 23. Ex: if the date and time is currently 2024-03-02 13:12:39 GMT, then the forecasts will cover
            the range from 2024-03-02 13:00:00 GMT to 2024-03-03 12:00:00 GMT.

            Args:
                geolocation: The geolocation for which to get data.
            """
            request = snug.Request(
                "GET", f"{_API_PREFIX}/v3/power-production-breakdown/forecast"
            )

            params = _geolocation_to_params(geolocation)

            return (yield request.with_params(params))

    class power_consumption_breakdown:
        # TODO(avianello): requires commercial auth
        @staticmethod
        @rest_query(response_schema=schemas.PowerConsumptionBreakdownForecast)
        def get_forecast(geolocation: Geolocation) -> Query[snug.Response]:
            """This endpoint retrieves the forecasted power consumption breakdown of an area, which represents the physical
            origin of electricity broken down by production type.

            The endpoint returns 24 hours of forecasts. The forecasts span from horizon 0, which is the start of the current
            hour, to horizon 23. Ex: if the date and time is currently 2024-03-02 13:12:39 GMT, then the forecasts will cover
            the range from 2024-03-02 13:00:00 GMT to 2024-03-03 12:00:00 GMT.

            Args:
                geolocation: The geolocation for which to get data.
            """
            request = snug.Request(
                "GET", f"{_API_PREFIX}/v3/power-consumption-breakdown/forecast"
            )

            params = _geolocation_to_params(geolocation)

            return (yield request.with_params(params))

    # TODO(avianello): requires commercial auth
    @staticmethod
    @rest_query(response_schema=schemas.Updates)
    def get_updated_since(
        geolocation: Geolocation,
        since: datetime,
        start: datetime | None = None,
        end: datetime | None = None,
        limit: int | None = None,
        threshold: str | None = None,
        disable_estimations: bool | None = None,
    ) -> Query[snug.Response]:
        """This endpoint returns a list of timestamps where data has been updated since a specified date for a specified zone.

        Access to this endpoint is only authorized if the token has access to one or more 'past' endpoints.

        Args:
            geolocation: The geolocation for which to get data.
            since: The datetime since which to get update timestamps.
            start (optional): A start datetime to specify a limited timeframe in which to search.
            end (optional): A end datetime to specify a limited timeframe in which to search get data.
            limit (optional): The limit of the number of entries to output (max 1000).
            threshold (optional): A duration in ISO 8601 format by which to filter entries to include only those where the
                difference between their timestamp and 'updated_at' is higher than 'threshold'. For example 'P1D'.
            disable_estimations (optional): Whether estimated data should be disabled.
        """
        request = snug.Request("GET", f"{_API_PREFIX}/v3/updated-since")

        params = _geolocation_to_params(geolocation)
        params.update(since=_as_utc_isoformat(since))
        if start is not None:
            params.update(start=_as_utc_isoformat(start))
        if end is not None:
            params.update(end=_as_utc_isoformat(end))
        if limit is not None:
            params.update(limit=limit)
        if threshold is not None:
            params.update(threshold=threshold)
        if disable_estimations is not None:
            params.update(disableEstimations=disable_estimations)

        return (yield request.with_params(params))
