import unittest
import requests
import os
import boto3

class TestAuhtenticatedApiEndpoint(unittest.TestCase):

    def setUp(self):
        self.base_url = os.getenv("HUSH_APIGW_URL")
        if not self.base_url:
            self.fail("Environment variable 'HUSH_APIGW_URL' is not set.")
        self.base_url = self.base_url + '/v1'

        self.test_user_username = os.getenv("HUSH_TEST_USER_USERNAME")
        if not self.test_user_username:
            self.fail("Environment variable 'HUSH_TEST_USER_USERNAME' is not set.")

        self.test_user_passwd = os.getenv("HUSH_TEST_USER_PASSWD")
        if not self.test_user_passwd:
            self.fail("Environment variable 'HUSH_TEST_USER_PASSWD' is not set.")

        self.region = self.user_pool.split('_')[0]

    def authenticate_with_cognito(self):
        client = boto3.client("cognito-idp")

        try:
            response = client.initiate_auth(
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={
                    "USERNAME": self.test_user_username,
                    "PASSWORD": self.test_user_passwd
                },
                ClientId=self.user_pool_client_id
            )

            if response.get("ChallengeName") == "NEW_PASSWORD_REQUIRED":
                print("New password required. Responding to the challenge.")
                challenge_response = client.respond_to_auth_challenge(
                    ClientId=self.user_pool_client_id,
                    ChallengeName="NEW_PASSWORD_REQUIRED",
                    ChallengeResponses={
                        "USERNAME": self.test_user_username,
                        "NEW_PASSWORD": self.test_user_passwd,
                    },
                    Session=response["Session"]
                )
                print(challenge_response)
                print("Password updated successfully.")
                id_token = challenge_response["AuthenticationResult"]["IdToken"]
                return id_token
            else:
                # No challenges; return the ID token
                return response["AuthenticationResult"]["IdToken"]
        except client.exceptions.NotAuthorizedException:
            print("Invalid username or password")
            raise
        except client.exceptions.UserNotConfirmedException:
            print("User is not confirmed")
            raise

    def test_get_hello_with_authentication(self):
        id_token = self.authenticate_with_cognito()
        headers = {"Authorization": id_token}
        endpoint = f"{self.base_url}/helloauthenticated"
        response = requests.get(endpoint, headers=headers)

        self.assertEqual(response.status_code, 200, f"Expected 200 but got {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    unittest.main()
