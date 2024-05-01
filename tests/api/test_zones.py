import snug

from voltorb import electricity_maps, execute, schemas


def test_get_zones(fixture_mock_client):
    """That can get the v3/zones endpoint."""
    query = electricity_maps.get_zones()

    client = fixture_mock_client(snug.Response(200, MOCK_GET_ZONES_RESPONSE))

    response = execute(query, client=client)
    assert client.request.url.endswith("v3/zones")

    # schemas.Zones is a parametrised generic so just check dict items instead
    assert isinstance(response, dict)
    assert all(
        isinstance(zone_metadata, schemas.ZoneMetadata)
        for zone_metadata in response.values()
    )


MOCK_GET_ZONES_RESPONSE = b"""\
{
  "AD": {
    "zoneName": "Andorra"
  },
  "AE": {
    "zoneName": "United Arab Emirates"
  },
  "US-CAR-DUK": {
    "countryName": "United States of America",
    "zoneName": "Duke Energy Carolinas"
  }
}
"""
