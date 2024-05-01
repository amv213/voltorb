from datetime import datetime, timedelta, timezone

import snug

from voltorb import ZoneKey, electricity_maps, execute, schemas


def test_get_latest(fixture_mock_client):
    """That can get the v3/power-breakdown/latest endpoint."""
    query = electricity_maps.power_breakdown.get_latest(geolocation=ZoneKey("FR"))

    client = fixture_mock_client(snug.Response(200, MOCK_GET_POWER_BREAKDOWN_LATEST))

    response = execute(query, client=client)
    assert client.request.url.endswith("v3/power-breakdown/latest")

    assert isinstance(response, schemas.PowerBreakdown)


def test_get_history(fixture_mock_client):
    """That can get the v3/power-breakdown/history endpoint."""
    query = electricity_maps.power_breakdown.get_history(geolocation=ZoneKey("DK-DK1"))

    client = fixture_mock_client(snug.Response(200, MOCK_GET_POWER_BREAKDOWN_HISTORY))

    response = execute(query, client=client)
    assert client.request.url.endswith("v3/power-breakdown/history")

    assert isinstance(response, schemas.PowerBreakdownHistory)


def test_get_past(fixture_mock_client):
    """That can get the v3/power-breakdown/past endpoint."""
    historical_datetime = datetime.now(timezone.utc) - timedelta(days=7)
    query = electricity_maps.power_breakdown.get_past(
        geolocation=ZoneKey("DK-DK1"), date_time=historical_datetime
    )

    client = fixture_mock_client(snug.Response(200, MOCK_GET_POWER_BREAKDOWN_PAST))

    response = execute(query, client=client)
    assert client.request.url.endswith("v3/power-breakdown/past")

    assert isinstance(response, schemas.PowerBreakdown)


def test_get_past_range(fixture_mock_client):
    """That can get the v3/power-breakdown/past-range endpoint."""
    start_historical_datetime = datetime.now(timezone.utc) - timedelta(days=7)
    end_historical_datetime = start_historical_datetime + timedelta(days=3)
    query = electricity_maps.power_breakdown.get_past_range(
        geolocation=ZoneKey("DE"),
        start=start_historical_datetime,
        end=end_historical_datetime,
    )

    client = fixture_mock_client(
        snug.Response(200, MOCK_GET_POWER_BREAKDOWN_PAST_RANGE)
    )

    response = execute(query, client=client)
    assert client.request.url.endswith("v3/power-breakdown/past-range")

    assert isinstance(response, schemas.PowerBreakdownRange)


def test_get_forecast(fixture_mock_client):
    """That can get the v3/power-breakdown/forecast endpoint."""
    query = electricity_maps.power_breakdown.get_forecast(geolocation=ZoneKey("DE"))
    client = fixture_mock_client(snug.Response(200, MOCK_GET_POWER_BREAKDOWN_FORECAST))

    response = execute(query, client=client)
    assert client.request.url.endswith("v3/power-breakdown/forecast")

    assert isinstance(response, schemas.PowerBreakdownForecast)


MOCK_GET_POWER_BREAKDOWN_LATEST = b"""\
{
  "zone": "FR",
  "datetime": "2022-04-20T09:00:00.000Z",
  "updatedAt": "2022-04-20T06:40:32.246Z",
  "createdAt": "2022-04-14T17:30:23.620Z",
  "powerConsumptionBreakdown": {
    "nuclear": 31479,
    "geothermal": 0,
    "biomass": 753,
    "coal": 227,
    "wind": 8122,
    "solar": 4481,
    "hydro": 7106,
    "gas": 6146,
    "oil": 341,
    "unknown": 2,
    "hydro discharge": 1013,
    "battery discharge": 0
  },
  "powerProductionBreakdown": {
    "nuclear": 31438,
    "geothermal": null,
    "biomass": 740,
    "coal": 219,
    "wind": 8034,
    "solar": 4456,
    "hydro": 7099,
    "gas": 6057,
    "oil": 341,
    "unknown": null,
    "hydro discharge": 1012,
    "battery discharge": null
  },
  "powerImportBreakdown": {
    "GB": 548
  },
  "powerExportBreakdown": {
    "GB": 0
  },
  "fossilFreePercentage": 89,
  "renewablePercentage": 36,
  "powerConsumptionTotal": 59670,
  "powerProductionTotal": 59396,
  "powerImportTotal": 548,
  "powerExportTotal": 0,
  "isEstimated": true,
  "estimationMethod": "TIME_SLICER_AVERAGE"
}
"""


MOCK_GET_POWER_BREAKDOWN_HISTORY = b"""\
{
  "zone": "DK-DK1",
  "history": [
    {
      "zone": "DK-DK1",
      "datetime": "2018-04-24T19:00:00.000Z",
      "updatedAt": "2018-04-24T19:00:00.000Z",
      "createdAt": "2018-04-24T19:00:00.000Z",
      "fossilFreePercentage": 75,
      "powerConsumptionBreakdown": {
        "biomass": 81,
        "coal": 395,
        "gas": 213,
        "geothermal": 0,
        "hydro": 521,
        "hydro discharge": 0,
        "battery discharge": null,
        "nuclear": 0,
        "oil": 9,
        "solar": 2,
        "unknown": 10,
        "wind": 1288
      },
      "powerConsumptionTotal": 2519,
      "powerImportBreakdown": {
        "DE": 0,
        "DK-DK1": 495,
        "SE": 445
      },
      "powerImportTotal": 940,
      "powerExportBreakdown": {
        "DE": 35,
        "DK-DK1": 0,
        "SE": 0
      },
      "powerExportTotal": 35,
      "powerProductionBreakdown": {
        "battery discharge": null,
        "biomass": 666,
        "coal": 260,
        "gas": 213,
        "geothermal": 0,
        "hydro": 0,
        "hydro discharge": null,
        "nuclear": 0,
        "oil": 24,
        "solar": 0,
        "unknown": 0,
        "wind": 176
      },
      "powerProductionTotal": 1339,
      "renewablePercentage": 75,
      "isEstimated": false,
      "estimationMethod": null
    }
  ]
}
"""


MOCK_GET_POWER_BREAKDOWN_PAST = b"""\
{
  "zone": "DK-DK1",
  "datetime": "2020-01-04T00:00:00.000Z",
  "updatedAt": "2022-04-07T09:35:03.914Z",
  "createdAt": "2022-02-04T15:49:58.284Z",
  "powerConsumptionBreakdown": {
    "nuclear": 65,
    "geothermal": 0,
    "biomass": 188,
    "coal": 195,
    "wind": 1642,
    "solar": 0,
    "hydro": 13,
    "gas": 72,
    "oil": 8,
    "unknown": 5,
    "hydro discharge": 0,
    "battery discharge": 0
  },
  "powerProductionBreakdown": {
    "nuclear": null,
    "geothermal": null,
    "biomass": 319,
    "coal": 287,
    "wind": 3088,
    "solar": 0,
    "hydro": 2,
    "gas": 97,
    "oil": 10,
    "unknown": 3,
    "hydro discharge": null,
    "battery discharge": null
  },
  "powerImportBreakdown": {
    "DE": 1070,
    "NL": 0,
    "SE": 0,
    "DK-DK2": 0,
    "NO-NO2": 0
  },
  "powerExportBreakdown": {
    "DE": 0,
    "NL": 700,
    "SE": 12,
    "DK-DK2": 589,
    "NO-NO2": 1387
  },
  "fossilFreePercentage": 87,
  "renewablePercentage": 84,
  "powerConsumptionTotal": 2188,
  "powerProductionTotal": 3806,
  "powerImportTotal": 1070,
  "powerExportTotal": 2687,
  "isEstimated": false,
  "estimationMethod": null
}
"""


MOCK_GET_POWER_BREAKDOWN_PAST_RANGE = b"""\
{
  "zone": "DE",
  "data": [
    {
      "zone": "DK-DK1",
      "datetime": "2020-01-04T00:00:00.000Z",
      "updatedAt": "2022-04-07T09:35:03.914Z",
      "createdAt": "2022-02-04T15:49:58.284Z",
      "powerConsumptionBreakdown": {
        "nuclear": 65,
        "geothermal": 0,
        "biomass": 188,
        "coal": 195,
        "wind": 1642,
        "solar": 0,
        "hydro": 13,
        "gas": 72,
        "oil": 8,
        "unknown": 5,
        "hydro discharge": 0,
        "battery discharge": 0
      },
      "powerProductionBreakdown": {
        "nuclear": null,
        "geothermal": null,
        "biomass": 319,
        "coal": 287,
        "wind": 3088,
        "solar": 0,
        "hydro": 2,
        "gas": 97,
        "oil": 10,
        "unknown": 3,
        "hydro discharge": null,
        "battery discharge": null
      },
      "powerImportBreakdown": {
        "DE": 1070,
        "NL": 0,
        "SE": 0,
        "DK-DK2": 0,
        "NO-NO2": 0
      },
      "powerExportBreakdown": {
        "DE": 0,
        "NL": 700,
        "SE": 12,
        "DK-DK2": 589,
        "NO-NO2": 1387
      },
      "fossilFreePercentage": 87,
      "renewablePercentage": 84,
      "powerConsumptionTotal": 2188,
      "powerProductionTotal": 3806,
      "powerImportTotal": 1070,
      "powerExportTotal": 2687,
      "isEstimated": false,
      "estimationMethod": null
    }
  ]
}
"""


MOCK_GET_POWER_BREAKDOWN_FORECAST = b"""\
{
  "zone": "DE",
  "data": [
    {
      "zone": "DE",
      "datetime": "2022-06-01T13:00:00.000Z",
      "updatedAt": "2022-06-01T13:00:00.000Z",
      "createdAt": "2022-06-01T13:00:00.000Z",
      "powerConsumptionBreakdown": {
        "nuclear": 3624,
        "geothermal": 18,
        "biomass": 4734,
        "coal": 16987,
        "wind": 7724,
        "solar": 24355,
        "hydro": 2884,
        "gas": 6832,
        "oil": 12,
        "unknown": 344,
        "hydro discharge": 104,
        "battery discharge": 0
      },
      "powerProductionBreakdown": {
        "nuclear": 3624,
        "geothermal": 20,
        "biomass": 5151,
        "coal": 18753,
        "wind": 8001,
        "solar": 27053,
        "hydro": 1879,
        "gas": 7376,
        "oil": 8,
        "unknown": 346,
        "hydro discharge": -2466,
        "battery discharge": null
      },
      "powerImportBreakdown": {},
      "powerExportBreakdown": {},
      "fossilFreePercentage": 64,
      "renewablePercentage": 59,
      "powerConsumptionTotal": 67618,
      "powerProductionTotal": 72211,
      "powerImportTotal": null,
      "powerExportTotal": null,
      "isEstimated": null,
      "estimationMethod": null
    },
    {
      "zone": "DE",
      "datetime": "2022-06-01T19:00:00.000Z",
      "updatedAt": "2022-06-01T19:00:00.000Z",
      "createdAt": "2022-06-01T19:00:00.000Z",
      "powerConsumptionBreakdown": {
        "nuclear": 3624,
        "geothermal": 18,
        "biomass": 4734,
        "coal": 16987,
        "wind": 7724,
        "solar": 24355,
        "hydro": 2884,
        "gas": 6832,
        "oil": 12,
        "unknown": 344,
        "hydro discharge": 104,
        "battery discharge": 0
      },
      "powerProductionBreakdown": {
        "nuclear": 3624,
        "geothermal": 20,
        "biomass": 5151,
        "coal": 18753,
        "wind": 8001,
        "solar": 27053,
        "hydro": 1879,
        "gas": 7376,
        "oil": 8,
        "unknown": 346,
        "hydro discharge": -2466,
        "battery discharge": null
      },
      "powerImportBreakdown": {},
      "powerExportBreakdown": {},
      "fossilFreePercentage": 64,
      "renewablePercentage": 59,
      "powerConsumptionTotal": 67618,
      "powerProductionTotal": 72211,
      "powerImportTotal": null,
      "powerExportTotal": null,
      "isEstimated": null,
      "estimationMethod": null
    }
  ]
}
"""
