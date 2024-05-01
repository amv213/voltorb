import pytest
import snug


class MockClient:
    """A mock client that returns canned responses and keep tracks."""

    def __init__(self, *responses: snug.Response) -> None:
        self.requests: list[snug.Request] = []
        self.responses = iter(responses)

        self.request: snug.Request | None = None
        self.response: snug.Response | None = None

    def send(self, req: snug.Request) -> snug.Response:
        self.requests.append(req)
        self.request = req

        self.response = next(self.responses)

        return self.response


snug.send.register(MockClient, MockClient.send)


@pytest.fixture()
def fixture_mock_client() -> type[MockClient]:
    """A mock client class to be instantiated by tests in the suite."""
    return MockClient
