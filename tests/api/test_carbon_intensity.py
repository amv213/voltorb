from datetime import datetime, timedelta, timezone

import pytest
import snug

from voltorb import Coordinates, ZoneKey, electricity_maps, execute, schemas

mock_geolocations = [ZoneKey("DE"), Coordinates(latitude=0, longitude=0)]


@pytest.mark.parametrize("geolocation", mock_geolocations)
def test_get_latest(fixture_mock_client, geolocation):
    """That can get the v3/carbon-intensity/latest endpoint."""
    query = electricity_maps.carbon_intensity.get_latest(geolocation)

    client = fixture_mock_client(snug.Response(200, MOCK_GET_CARBON_INTENSITY_LATEST))

    response = execute(query, client=client)
    assert client.request.url.endswith("v3/carbon-intensity/latest")

    assert isinstance(response, schemas.CarbonIntensity)


@pytest.mark.parametrize("geolocation", mock_geolocations)
def test_get_history(fixture_mock_client, geolocation):
    """That can get the v3/carbon-intensity/history endpoint."""
    query = electricity_maps.carbon_intensity.get_history(geolocation)

    client = fixture_mock_client(snug.Response(200, MOCK_GET_CARBON_INTENSITY_HISTORY))

    response = execute(query, client=client)
    assert client.request.url.endswith("v3/carbon-intensity/history")

    assert isinstance(response, schemas.CarbonIntensityHistory)


@pytest.mark.parametrize("geolocation", mock_geolocations)
def test_get_past(fixture_mock_client, geolocation):
    """That can get the v3/carbon-intensity/past endpoint."""
    historical_datetime = datetime.now(timezone.utc) - timedelta(days=7)
    query = electricity_maps.carbon_intensity.get_past(
        geolocation, date_time=historical_datetime
    )

    client = fixture_mock_client(snug.Response(200, MOCK_GET_CARBON_INTENSITY_PAST))

    response = execute(query, client=client)
    assert client.request.url.endswith("v3/carbon-intensity/past")

    assert isinstance(response, schemas.CarbonIntensity)


@pytest.mark.parametrize("geolocation", mock_geolocations)
def test_get_past_range(fixture_mock_client, geolocation):
    """That can get the v3/carbon-intensity/past-range endpoint."""
    start_historical_datetime = datetime.now(timezone.utc) - timedelta(days=7)
    end_historical_datetime = start_historical_datetime + timedelta(days=3)
    query = electricity_maps.carbon_intensity.get_past_range(
        geolocation,
        start=start_historical_datetime,
        end=end_historical_datetime,
    )

    client = fixture_mock_client(
        snug.Response(200, MOCK_GET_CARBON_INTENSITY_PAST_RANGE)
    )

    response = execute(query, client=client)
    assert client.request.url.endswith("v3/carbon-intensity/past-range")

    assert isinstance(response, schemas.CarbonIntensityRange)


@pytest.mark.parametrize("geolocation", mock_geolocations)
def test_get_forecast(fixture_mock_client, geolocation):
    """That can get the v3/carbon-intensity/forecast endpoint."""
    query = electricity_maps.carbon_intensity.get_forecast(geolocation)
    client = fixture_mock_client(snug.Response(200, MOCK_GET_CARBON_INTENSITY_FORECAST))

    response = execute(query, client=client)
    assert client.request.url.endswith("v3/carbon-intensity/forecast")

    assert isinstance(response, schemas.CarbonIntensityForecast)


MOCK_GET_CARBON_INTENSITY_LATEST = b"""\
{
  "zone": "DE",
  "carbonIntensity": 302,
  "datetime": "2018-04-25T18:07:00.350Z",
  "updatedAt": "2018-04-25T18:07:01.000Z",
  "createdAt": "2018-04-25T18:07:01.000Z",
  "emissionFactorType": "lifecycle",
  "isEstimated": true,
  "estimationMethod": "TIME_SLICER_AVERAGE"
}
"""


MOCK_GET_CARBON_INTENSITY_HISTORY = b"""\
{
  "zone": "DE",
  "history": [
    {
      "zone": "DE",
      "carbonIntensity": 413,
      "datetime": "2021-08-18T13:00:00.000Z",
      "updatedAt": "2021-08-19T08:40:20.886Z",
      "createdAt": "2021-08-15T13:40:15.544Z",
      "emissionFactorType": "lifecycle",
      "isEstimated": false,
      "estimationMethod": null
    },
    {
      "zone": "DE",
      "carbonIntensity": 338,
      "datetime": "2021-08-19T12:00:00.000Z",
      "updatedAt": "2021-08-19T12:39:55.666Z",
      "createdAt": "2021-08-16T12:39:45.450Z",
      "emissionFactorType": "lifecycle",
      "isEstimated": false,
      "estimationMethod": null
    }
  ]
}
"""


MOCK_GET_CARBON_INTENSITY_PAST = b"""\
{
  "zone": "DE",
  "carbonIntensity": 322,
  "datetime": "2019-05-21T00:00:00.000Z",
  "updatedAt": "2022-04-07T15:32:21.002Z",
  "createdAt": "2022-02-08T06:20:31.772Z",
  "emissionFactorType": "lifecycle",
  "isEstimated": false,
  "estimationMethod": null
}
"""


MOCK_GET_CARBON_INTENSITY_PAST_RANGE = b"""\
{
  "zone": "DE",
  "data": [
    {
      "zone": "DE",
      "carbonIntensity": 339,
      "datetime": "2019-05-21T21:00:00.000Z",
      "updatedAt": "2022-04-07T15:32:36.348Z",
      "createdAt": "2022-02-08T06:20:31.772Z",
      "emissionFactorType": "lifecycle",
      "isEstimated": false,
      "estimationMethod": null
    },
    {
      "zone": "DE",
      "carbonIntensity": 317,
      "datetime": "2019-05-21T22:00:00.000Z",
      "updatedAt": "2022-04-07T15:32:36.348Z",
      "createdAt": "2022-02-08T06:17:02.676Z",
      "emissionFactorType": "lifecycle",
      "isEstimated": false,
      "estimationMethod": null
    },
    {
      "zone": "DE",
      "carbonIntensity": 305,
      "datetime": "2019-05-21T23:00:00.000Z",
      "updatedAt": "2022-04-07T15:32:36.348Z",
      "createdAt": "2022-02-08T06:17:21.012Z",
      "emissionFactorType": "lifecycle",
      "isEstimated": false,
      "estimationMethod": null
    }
  ]
}
"""


MOCK_GET_CARBON_INTENSITY_FORECAST = b"""\
{
  "zone": "DK-DK2",
  "forecast": [
    {
      "carbonIntensity": 326,
      "datetime": "2018-11-26T17:00:00.000Z"
    },
    {
      "carbonIntensity": 297,
      "datetime": "2018-11-26T18:00:00.000Z"
    },
    {
      "carbonIntensity": 194,
      "datetime": "2018-11-28T17:00:00.000Z"
    }
  ],
  "updatedAt": "2018-11-26T17:25:24.685Z"
}
"""
