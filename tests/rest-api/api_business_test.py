import requests
from api_base import TestApiBase

class TestApiBusinessEndpoints(TestApiBase):

    def _store_results(self, body):
        endpoint = f"{self.base_url}/tournament/match"
        id_token = self.authenticate_with_cognito()
        headers = {"Authorization": id_token}
        response = requests.put(endpoint, headers=headers, json=body)
        self.assertEqual(response.status_code, 200, f"Expected 200 but got {response.status_code}")

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

    def test_store_and_retrieve_results(self):
        tournament_id = "MyTournament" + self.create_unique_identifier()
        match_id1 = self.create_unique_identifier()
        match_id2 = self.create_unique_identifier()

        body1 = {
            "tournament_id": tournament_id,
            "match_id": match_id1,
            "player1": "Steven",
            "player2": "Robert",
            "score": "5,4,9",
        }
        body2 = {
            "tournament_id": tournament_id,
            "match_id": match_id2,
            "player1": "James",
            "player2": "Frank",
            "score": "6,-4,7,10",
        }

        self._store_results(body1)
        self._store_results(body2)

        get_endpoint = f"{self.base_url}/tournament/{tournament_id}/results"
        response = requests.get(get_endpoint)
        #print(response.text)
        self.assertEqual(response.status_code, 200, f"Expected 200 but got {response.status_code}")

        parsed_response = response.json()
        results = parsed_response.get("results", [])

        nb_of_results = len(results)
        self.assertEqual(nb_of_results, 2, f"Expected 2 results but got back {nb_of_results}")

        # ToDo: To be thorought we should check for the actual return values also
