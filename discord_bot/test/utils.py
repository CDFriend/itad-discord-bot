class MockJSONResponse:
    """Mocked JSON response for requests calls."""
    def __init__(self, data: dict):
        self._json_data = data

    def json(self):
        return self._json_data
