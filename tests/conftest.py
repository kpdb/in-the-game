import pytest
from starlette.testclient import TestClient

from in_the_game.api import app


@pytest.fixture(scope="module")
def test_app():
    yield TestClient(app)
