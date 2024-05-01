import snug

from voltorb import electricity_maps, execute, schemas

MOCK_GET_HEALTH_RESPONSE = b"""\
{
  "monitors": {
    "state": "ok"
  },
  "status": "ok"
}
"""


def test_get_health(fixture_mock_client):
    """That can get the /health endpoint."""
    client = fixture_mock_client(snug.Response(200, MOCK_GET_HEALTH_RESPONSE))

    query = electricity_maps.get_health()
    response = execute(query, client=client)
    assert isinstance(response, schemas.Health)
