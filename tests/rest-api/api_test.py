import unittest
import requests
from api_base import TestApiBase

class TestApiEndpoint(TestApiBase):

    def test_get_hello_endpoint(self):
        endpoint = f"{self.base_url}/hello"
        response = requests.get(endpoint)

        self.assertEqual(response.status_code, 200, f"Expected 200 but got {response.status_code}")

        expected_substring = "Hush"
        self.assertIn(expected_substring, response.text, f"'{expected_substring}' not found in response body")

    def test_get_hello_region(self):
        endpoint = f"{self.base_url}/hello"
        response = requests.get(endpoint)

        self.assertEqual(response.status_code, 200, f"Expected 200 but got {response.status_code}")

        expected_region = self.aws_reqion
        self.assertIn(expected_region, response.text, f"'{expected_region}' not found in response body")

    def test_get_hello_missing_authentication(self):
        endpoint = f"{self.base_url}/helloauthenticated"
        response = requests.get(endpoint)

        self.assertEqual(response.status_code, 401, f"Expected 401 but got {response.status_code}")

    def test_missing_endpoint(self):
        endpoint = f"{self.base_url}/notrealendpoint"
        response = requests.get(endpoint)

        # ApiGw returns 403 for endpoints that don't exist
        self.assertEqual(response.status_code, 403, f"Expected 403 but got {response.status_code}")

if __name__ == "__main__":
    unittest.main()
