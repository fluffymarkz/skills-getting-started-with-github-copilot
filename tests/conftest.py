import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app

INITIAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """Ensure each test runs with a clean in-memory activities store."""
    activities.clear()
    activities.update(copy.deepcopy(INITIAL_ACTIVITIES))
    yield
    activities.clear()
    activities.update(copy.deepcopy(INITIAL_ACTIVITIES))


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def existing_activity_name():
    return "Chess Club"


@pytest.fixture
def new_email():
    return "test.student@mergington.edu"


@pytest.fixture
def existing_participant_email():
    return "michael@mergington.edu"
