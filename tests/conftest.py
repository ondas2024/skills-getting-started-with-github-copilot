from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def original_activities():
    snapshot = deepcopy(activities)
    try:
        yield snapshot
    finally:
        activities.clear()
        activities.update(snapshot)


@pytest.fixture
def client(original_activities):
    with TestClient(app) as test_client:
        yield test_client
