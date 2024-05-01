from datetime import datetime, timezone

import snug

from voltorb import ZoneKey, electricity_maps, execute, schemas


def test_get_health(fixture_mock_client):
    """That can get the v3/updated-since endpoint."""
    since = datetime.now(timezone.utc)
    query = electricity_maps.get_updated_since(
        geolocation=ZoneKey("DK-DK1"), since=since
    )

    client = fixture_mock_client(snug.Response(200, MOCK_GET_UPDATED_SINCE))

    response = execute(query, client=client)
    assert isinstance(response, schemas.Updates)


MOCK_GET_UPDATED_SINCE = b"""\
{
  "zone": "DK-DK1",
  "updates": [
    {
      "updatedAt": "2020-02-07T11:54:55.581Z",
      "datetime": "2020-02-05T00:00:00.000Z"
    },
    {
      "updatedAt": "2020-02-07T11:54:55.581Z",
      "datetime": "2020-02-05T23:00:00.000Z"
    },
    {
      "updatedAt": "2020-02-07T11:54:55.581Z",
      "datetime": "2020-02-05T00:00:00.000Z"
    }
  ],
  "threshold": "P1D",
  "limit": 100,
  "limitReached": false
}

"""
