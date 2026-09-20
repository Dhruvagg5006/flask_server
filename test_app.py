import json
import unittest
from app import app

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_home_page(self):
        """Test that the homepage renders successfully with HTTP 200."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Flask App CI/CD Demo", response.data)
        self.assertIn(b"AWS EC2", response.data)

    def test_health_endpoint(self):
        """Test that the health endpoint returns status healthy with JSON 200."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "healthy")
        self.assertIn("version", data)
        self.assertIn("timestamp", data)

    def test_api_info_endpoint(self):
        """Test the api info endpoint returns expected project details."""
        response = self.client.get("/api/info")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["project"], "Flask CI/CD on AWS EC2")
        self.assertEqual(data["status"], "running")

    def test_404_error(self):
        """Test non-existent routes return 404."""
        response = self.client.get("/non-existent-page")
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
