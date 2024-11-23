from aws_cdk import (
    Stack,
    Construct,
    aws_cognito as cognito
)

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
