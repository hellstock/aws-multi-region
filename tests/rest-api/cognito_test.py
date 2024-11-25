import unittest
import os
import boto3
from datetime import datetime

# This does not need to be actual working e-mail in our set-up
BASE_EMAIL = "user@hush.com"
TEMPORARY_PASSWORD = "SecurePassword123!"

class TestCognito(unittest.TestCase):

    def setUp(self):
        self.user_pool = os.getenv("HUSH_USER_POOL_ID")
        if not self.user_pool:
            self.fail("Environment variable 'HUSH_USER_POOL_ID' is not set.")

        self.user_pool_client_id = os.getenv("HUSH_USER_POOL_CLIENT_ID")
        if not self.user_pool_client_id:
            self.fail("Environment variable 'HUSH_USER_POOL_CLIENT_ID' is not set.")

        self.region = self.user_pool.split('_')[0]

    # The postfix parameter is used to distinguish aliases created on same second when
    # all test cases are run. Otherwise later cases fail with "user already exists"
    def create_new_email_alias(self, base_email,postfix=""):
        local_part, domain = base_email.split("@")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_email = f"{local_part}+{timestamp}{postfix}@{domain}"
        return unique_email

    def sign_up_user(self, client, user_pool_client_id, email, password):
        response = client.sign_up(
            ClientId=user_pool_client_id,
            Username=email,
            Password=password,
            UserAttributes=[
                {"Name": "email", "Value": email},
            ]
        )

        return response

    def test_admin_create_user(self):
        email = self.create_new_email_alias(BASE_EMAIL, "a")
        client = boto3.client('cognito-idp', region_name=self.region)

        response = client.admin_create_user(
            UserPoolId=self.user_pool,
            Username=email,
            UserAttributes=[
                {"Name": "email", "Value": email},
                {"Name": "email_verified", "Value": "true"}
            ],
            TemporaryPassword=TEMPORARY_PASSWORD,
            MessageAction="SUPPRESS"
        )

        self.assertIn('User', response, "Response does not contain 'User' field")
        user_attributes = response['User'].get('Attributes', [])
        email_attribute = next(
            (attr for attr in user_attributes if attr['Name'] == 'email'), None
        )

        self.assertIsNotNone(email_attribute, "Email attribute is missing in the response")

        self.assertEqual(
            email_attribute['Value'], email,
            f"Expected email {email}, but got {email_attribute['Value']}"
        )

    def test_user_sign_up(self):
        user_pool_client_id = self.user_pool_client_id
        email = self.create_new_email_alias(BASE_EMAIL, "s")
        password = TEMPORARY_PASSWORD

        client = boto3.client("cognito-idp")

        try:
            response = self.sign_up_user(client, user_pool_client_id, email, password)
            # print("User signed up successfully!")
            # print(response)
        except client.exceptions.UsernameExistsException:
            self.fail("User already exists")
        except Exception as e:
            self.fail(f"An error occurred: {e}")