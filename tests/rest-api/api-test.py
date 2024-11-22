import unittest
import requests
import os

class TestApiEndpoint(unittest.TestCase):

    def setUp(self):
        self.base_url = os.getenv("HUSH_APIGW_URL")
        if not self.base_url:
            self.fail("Environment variable 'HUSH_APIGW_URL' is not set.")

    def test_get_hello_endpoint(self):
        endpoint = f"{self.base_url}/hello"
        response = requests.get(endpoint)
        
        self.assertEqual(response.status_code, 200, f"Expected 200 but got {response.status_code}")

        expected_substring = "Hush"
        self.assertIn(expected_substring, response.text, f"'{expected_substring}' not found in response body")

if __name__ == "__main__":
    unittest.main()
