import unittest
import os
import boto3
from datetime import datetime

# This does not need to be actual working e-mail in our set-up
BASE_EMAIL = "user@hush.com"

class TestCognito(unittest.TestCase):

    def setUp(self):
        self.user_pool = os.getenv("HUSH_USER_POOL_ID")
        if not self.user_pool:
            self.fail("Environment variable 'HUSH_USER_POOL_ID' is not set.")

        self.region = self.user_pool.split('_')[0]

    def create_new_email_alias(self, base_email):
        local_part, domain = base_email.split("@")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_email = f"{local_part}+{timestamp}@{domain}"
        return unique_email

    def test_admin_create_user(self):
        email = self.create_new_email_alias(BASE_EMAIL)
        client = boto3.client('cognito-idp', region_name=self.region)

        response = client.admin_create_user(
            UserPoolId=self.user_pool,
            Username=email,
            UserAttributes=[
                {"Name": "email", "Value": email},
                {"Name": "email_verified", "Value": "true"}
            ],
            TemporaryPassword="TempPassword123!",
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

        # print("User created:", response)
