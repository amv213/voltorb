import snug

from voltorb import ZoneKey, electricity_maps, execute, schemas


def test_get_forecast(fixture_mock_client):
    """That can get the v3/power-consumption-breakdown/forecast endpoint."""
    query = electricity_maps.power_consumption_breakdown.get_forecast(
        geolocation=ZoneKey("DK-DK2")
    )

    client = fixture_mock_client(
        snug.Response(200, MOCK_GET_POWER_PRODUCTION_BREAKDOWN_FORECAST)
    )

    response = execute(query, client=client)
    assert client.request.url.endswith("v3/power-consumption-breakdown/forecast")

    assert isinstance(response, schemas.PowerConsumptionBreakdownForecast)


MOCK_GET_POWER_PRODUCTION_BREAKDOWN_FORECAST = b"""\
{
  "zone": "DK-DK2",
  "forecast": [
    {
      "powerConsumptionBreakdown": {
        "biomass": 483,
        "coal": 475,
        "gas": 338,
        "geothermal": 0,
        "hydro": 632,
        "nuclear": 383,
        "solar": 4,
        "oil": 0,
        "wind": 188,
        "unknown": 69,
        "hydro discharge": null,
        "battery discharge": null
      },
      "datetime": "2018-11-26T17:00:00.000Z",
      "powerConsumptionTotal": 2572
    },
    {
      "powerConsumptionBreakdown": {
        "biomass": 459,
        "coal": 441,
        "gas": 308,
        "geothermal": 0,
        "hydro": 639,
        "nuclear": 382,
        "solar": 0,
        "oil": 0,
        "wind": 167,
        "unknown": 68,
        "hydro discharge": null,
        "battery discharge": null
      },
      "datetime": "2018-11-26T18:00:00.000Z",
      "powerConsumptionTotal": 2464
    },
    {
      "powerConsumptionBreakdown": {
        "biomass": 158,
        "coal": 652,
        "gas": 385,
        "geothermal": 0,
        "hydro": 326,
        "nuclear": 169,
        "solar": 44,
        "oil": 0,
        "wind": 210,
        "unknown": 36,
        "hydro discharge": null,
        "battery discharge": null
      },
      "datetime": "2018-11-27T17:00:00.000Z",
      "powerConsumptionTotal": 1980
    }
  ],
  "updatedAt": "2018-11-26T17:26:57.091Z"
}
"""
