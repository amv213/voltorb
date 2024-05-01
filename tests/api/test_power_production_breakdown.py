import snug

from voltorb import ZoneKey, electricity_maps, execute, schemas


def test_get_forecast(fixture_mock_client):
    """That can get the v3/power-production-breakdown/forecast endpoint."""
    query = electricity_maps.power_production_breakdown.get_forecast(
        geolocation=ZoneKey("DE")
    )

    client = fixture_mock_client(
        snug.Response(200, MOCK_GET_POWER_PRODUCTION_BREAKDOWN_FORECAST)
    )

    response = execute(query, client=client)
    assert client.request.url.endswith("v3/power-production-breakdown/forecast")

    assert isinstance(response, schemas.PowerProductionBreakdownForecast)


MOCK_GET_POWER_PRODUCTION_BREAKDOWN_FORECAST = b"""\
{
  "zone": "DE",
  "forecast": [
    {
      "powerProductionBreakdown": {
        "nuclear": 4392,
        "geothermal": 0,
        "biomass": 5178,
        "coal": 25078,
        "wind": 7706,
        "solar": 28604,
        "hydro": 1659,
        "gas": 9602,
        "oil": 65,
        "unknown": 0,
        "hydro discharge": null,
        "battery discharge": null
      },
      "datetime": "2022-06-01T13:00:00.000Z",
      "powerProductionTotal": 82284
    },
    {
      "powerProductionBreakdown": {
        "nuclear": 4386,
        "geothermal": 0,
        "biomass": 5196,
        "coal": 25566,
        "wind": 7818,
        "solar": 23762,
        "hydro": 1711,
        "gas": 10312,
        "oil": 67,
        "unknown": 0,
        "hydro discharge": null,
        "battery discharge": null
      },
      "datetime": "2022-06-01T14:00:00.000Z",
      "powerProductionTotal": 78818
    }
  ],
  "updatedAt": "2022-06-01T12:55:37.578Z"
}
"""
