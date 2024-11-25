import unittest
import requests
import os

class TestApiBusinessEndpoints(unittest.TestCase):

    def setUp(self):
        self.base_url = os.getenv("HUSH_APIGW_URL")
        if not self.base_url:
            self.fail("Environment variable 'HUSH_APIGW_URL' is not set.")
        self.base_url = self.base_url + '/v1'

        self.aws_reqion = os.getenv("HUSH_AWS_REGION")
        if not self.aws_reqion:
            self.fail("Environment variable 'HUSH_AWS_REGION' is not set.")

    def test_get_results_endpoint(self):
        endpoint = f"{self.base_url}/tournament/12345/results"
        response = requests.get(endpoint)

        self.assertEqual(response.status_code, 200, f"Expected 200 but got {response.status_code}")
