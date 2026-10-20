from copy import deepcopy

from src.app import activities


def test_root_redirects_to_static_index(client, original_activities):
    expected_location = "/static/index.html"

    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == expected_location
    assert activities == original_activities


def test_get_activities_returns_complete_data(client, original_activities):
    expected = deepcopy(original_activities)

    response = client.get("/activities")

    assert response.status_code == 200
    assert response.json() == expected
    assert activities == original_activities


def test_signup_adds_only_selected_participant(client, original_activities):
    email = "new-student@mergington.edu"
    expected = deepcopy(original_activities)
    expected["Chess Club"]["participants"].append(email)
    expected_message = f"Signed up {email} for Chess Club"

    response = client.post(
        "/activities/Chess%20Club/signup", params={"email": email}
    )
    listing = client.get("/activities")

    assert response.status_code == 200
    assert response.json() == {"message": expected_message}
    assert activities == expected
    assert listing.status_code == 200
    assert listing.json() == expected


def test_signup_unknown_activity_returns_not_found(client, original_activities):
    url = "/activities/Unknown/signup"
    email = "new-student@mergington.edu"

    response = client.post(url, params={"email": email})

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
    assert activities == original_activities


def test_duplicate_signup_returns_bad_request(client, original_activities):
    url = "/activities/Chess%20Club/signup"
    email = original_activities["Chess Club"]["participants"][0]

    response = client.post(url, params={"email": email})

    assert response.status_code == 400
    assert response.json() == {"detail": "Student is already signed up"}
    assert activities == original_activities


def test_signup_missing_email_returns_validation_error(client, original_activities):
    url = "/activities/Chess%20Club/signup"

    response = client.post(url)

    assert response.status_code == 422
    assert any(
        error["loc"] == ["query", "email"]
        for error in response.json()["detail"]
    )
    assert activities == original_activities
