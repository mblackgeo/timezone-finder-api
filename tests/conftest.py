import pytest
from fastapi.testclient import TestClient

from tzfinderapi.api import app


@pytest.fixture(scope="session")
def client():
    yield TestClient(app)
