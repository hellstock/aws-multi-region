from aws_cdk import (
    Stack,
    aws_cognito as cognito
)
from constructs import Construct

class HushCognitoStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.user_pool = cognito.UserPool(
            self,
            "HushUserPool",
            user_pool_name="HushUserPool",
            self_sign_up_enabled=True,
            sign_in_aliases=cognito.SignInAliases(
                email=True,
                username=False
            ),
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(required=True, mutable=True)
            )
        )

        self.user_pool_client = cognito.UserPoolClient(
            self,
            "HushUserPoolClient",
            user_pool=self.user_pool,
            user_pool_client_name="HushAppClient",
            generate_secret=False,
            auth_flows=cognito.AuthFlow(
                user_password=True,
                admin_user_password=True
            )
        )
