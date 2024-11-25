import unittest
import requests
import os
from api_base import TestApiBase

class TestApiBusinessEndpoints(TestApiBase):

    def setUp(self):
        super.setUp()

    def test_get_results_endpoint(self):
        endpoint = f"{self.base_url}/tournament/12345/results"
        response = requests.get(endpoint)

        self.assertEqual(response.status_code, 200, f"Expected 200 but got {response.status_code}")
