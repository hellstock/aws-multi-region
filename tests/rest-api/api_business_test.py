import unittest
import requests
import os
from api_base import TestApiBase

class TestApiBusinessEndpoints(TestApiBase):

    def test_get_results_endpoint_non_existing_tournament(self):
        endpoint = f"{self.base_url}/tournament/12345/results"
        response = requests.get(endpoint)

        self.assertEqual(response.status_code, 404, f"Expected 404 but got {response.status_code}")

    def test_store_results_endpoint(self):
        endpoint = f"{self.base_url}/tournament/match"
        id_token = self.authenticate_with_cognito()
        headers = {"Authorization": id_token}

        body = {
            "tournament_id": "MyTournament2024",
            "match_id": "A1",
            "player1": "Frank",
            "player2": "James",
            "score": "5,4,9",
        }
        response = requests.post(endpoint, headers=headers, json=body)

        self.assertEqual(response.status_code, 200, f"Expected 200 but got {response.status_code}")
