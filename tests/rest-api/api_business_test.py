import requests
from api_base import TestApiBase

class TestApiBusinessEndpoints(TestApiBase):

    def test_get_results_endpoint_non_existing_tournament(self):
        endpoint = f"{self.base_url}/tournament/12345/results"
        response = requests.get(endpoint)

        self.assertEqual(response.status_code, 404, f"Expected 404 but got {response.status_code}")

    def test_post_result_incomplete_body(self):
        endpoint = f"{self.base_url}/tournament/match"
        id_token = self.authenticate_with_cognito()
        headers = {"Authorization": id_token}

        body = {
            "tournament_id": "MyTournament2024",
            "match_id": "A6",
            "player1": "Steven",
            "player2": "Robert",
            # "score": "5,4,9", Score missing on purpose
        }
        response = requests.post(endpoint, headers=headers, json=body)

        self.assertEqual(response.status_code, 400, f"Expected 400 but got {response.status_code}")


    def test_post_results_endpoint(self):
        endpoint = f"{self.base_url}/tournament/match"
        id_token = self.authenticate_with_cognito()
        headers = {"Authorization": id_token}

        match_id = self.create_unique_identifier()

        body = {
            "tournament_id": "MyTournament2024",
            "match_id": match_id,
            "player1": "Steven",
            "player2": "Robert",
            "score": "5,4,9",
        }
        response = requests.post(endpoint, headers=headers, json=body)

        self.assertEqual(response.status_code, 200, f"Expected 200 but got {response.status_code}")

    def test_put_results_endpoint(self):
        endpoint = f"{self.base_url}/tournament/match"
        id_token = self.authenticate_with_cognito()
        headers = {"Authorization": id_token}

        match_id = self.create_unique_identifier()

        body = {
            "tournament_id": "MyTournament2024",
            "match_id": match_id,
            "player1": "Steven",
            "player2": "Robert",
            "score": "5,4,9",
        }
        response = requests.put(endpoint, headers=headers, json=body)
        self.assertEqual(response.status_code, 200, f"First operation: Expected 200 but got {response.status_code}")

        # Let's check it also succeeds second time
        response = requests.put(endpoint, headers=headers, json=body)
        self.assertEqual(response.status_code, 200, f"Second operation: Expected 200 but got {response.status_code}")

