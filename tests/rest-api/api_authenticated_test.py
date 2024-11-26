import requests
from api_base import TestApiBase


class TestAuhtenticatedApiEndpoint(TestApiBase):

    def test_get_hello_with_authentication(self):
        id_token = self.authenticate_with_cognito()
        headers = {"Authorization": id_token}
        endpoint = f"{self.base_url}/helloauthenticated"
        response = requests.get(endpoint, headers=headers)

        self.assertEqual(
            response.status_code, 200,
            f"Expected 200 but got {response.status_code}")
        print(response.text)
