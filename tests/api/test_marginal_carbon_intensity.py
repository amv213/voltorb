from datetime import datetime, timedelta, timezone

import snug

from voltorb import ZoneKey, electricity_maps, execute, schemas


def test_get_past(fixture_mock_client):
    """That can get the v3/marginal-carbon-intensity/past endpoint."""
    historical_datetime = datetime.now(timezone.utc) - timedelta(days=7)
    query = electricity_maps.marginal_carbon_intensity.get_past(
        geolocation=ZoneKey("GB"), date_time=historical_datetime
    )

    client = fixture_mock_client(
        snug.Response(200, MOCK_GET_MARGINAL_CARBON_INTENSITY_PAST)
    )

    response = execute(query, client=client)
    assert client.request.url.endswith("v3/marginal-carbon-intensity/past")

    assert isinstance(response, schemas.CarbonIntensity)


def test_get_past_range(fixture_mock_client):
    """That can get the v3/marginal-carbon-intensity/past-range endpoint."""
    start_historical_datetime = datetime.now(timezone.utc) - timedelta(days=7)
    end_historical_datetime = start_historical_datetime + timedelta(days=3)
    query = electricity_maps.marginal_carbon_intensity.get_past_range(
        geolocation=ZoneKey("GB"),
        start=start_historical_datetime,
        end=end_historical_datetime,
    )

    client = fixture_mock_client(
        snug.Response(200, MOCK_GET_MARGINAL_CARBON_INTENSITY_PAST_RANGE)
    )

    response = execute(query, client=client)
    assert client.request.url.endswith("v3/marginal-carbon-intensity/past-range")

    assert isinstance(response, schemas.CarbonIntensityRange)


MOCK_GET_MARGINAL_CARBON_INTENSITY_PAST = b"""\
{
  "zone": "GB",
  "carbonIntensity": 359,
  "datetime": "2023-01-04T00:00:00.000Z",
  "updatedAt": "2023-10-01T18:30:28.708Z",
  "createdAt": "2023-07-06T12:57:18.612Z",
  "emissionFactorType": "lifecycle",
  "isEstimated": false,
  "estimationMethod": null
}
"""


MOCK_GET_MARGINAL_CARBON_INTENSITY_PAST_RANGE = b"""\
{
  "zone": "GB",
  "data": [
    {
      "zone": "GB",
      "carbonIntensity": 362,
      "datetime": "2023-01-04T01:00:00.000Z",
      "updatedAt": "2023-10-01T18:30:28.708",
      "createdAt": "2023-07-06T12:57:18.612Z",
      "emissionFactorType": "lifecycle",
      "isEstimated": false,
      "estimationMethod": null
    },
    {
      "zone": "GB",
      "carbonIntensity": 369,
      "datetime": "2023-01-04T02:00:00.000Z",
      "updatedAt": "2023-10-01T18:30:28.708",
      "createdAt": "2023-07-06T12:57:18.612Z",
      "emissionFactorType": "lifecycle",
      "isEstimated": false,
      "estimationMethod": null
    },
    {
      "zone": "GB",
      "carbonIntensity": 368,
      "datetime": "2023-01-04T03:00:00.000Z",
      "updatedAt": "2023-10-01T18:30:28.708",
      "createdAt": "2023-07-06T12:57:18.612Z",
      "emissionFactorType": "lifecycle",
      "isEstimated": false,
      "estimationMethod": null
    }
  ]
}
"""
