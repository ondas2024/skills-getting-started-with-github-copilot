from copy import deepcopy
import unittest

from fastapi.testclient import TestClient

from src.app import activities, app


class UnregisterTests(unittest.TestCase):
    def setUp(self):
        self.original_activities = deepcopy(activities)
        self.client = TestClient(app)
        self.url = "/activities/Chess%20Club/signup"
        self.email = activities["Chess Club"]["participants"][0]

    def tearDown(self):
        activities.clear()
        activities.update(self.original_activities)
        self.client.close()

    def test_unregister_removes_only_selected_participant(self):
        response = self.client.delete(self.url, params={"email": self.email})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"message": f"Unregistered {self.email} from Chess Club"},
        )
        expected = deepcopy(self.original_activities)
        expected["Chess Club"]["participants"].remove(self.email)
        self.assertEqual(self.client.get("/activities").json(), expected)

    def test_unknown_activity_returns_not_found(self):
        response = self.client.delete(
            "/activities/Unknown/signup", params={"email": self.email}
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Activity not found"})
        self.assertEqual(activities, self.original_activities)

    def test_unregistered_participant_returns_not_found(self):
        response = self.client.delete(
            self.url, params={"email": "not-registered@mergington.edu"}
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Student is not signed up"})
        self.assertEqual(activities, self.original_activities)

    def test_repeat_unregister_then_signup(self):
        self.assertEqual(
            self.client.delete(self.url, params={"email": self.email}).status_code,
            200,
        )
        self.assertEqual(
            self.client.delete(self.url, params={"email": self.email}).status_code,
            404,
        )
        self.assertEqual(
            self.client.post(self.url, params={"email": self.email}).status_code,
            200,
        )
        self.assertEqual(
            self.client.post(self.url, params={"email": self.email}).status_code,
            400,
        )

    def test_missing_email_returns_validation_error(self):
        self.assertEqual(self.client.delete(self.url).status_code, 422)
        self.assertEqual(activities, self.original_activities)
