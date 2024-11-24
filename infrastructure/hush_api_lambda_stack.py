import os

from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_cognito as cognito
)
from constructs import Construct
from aws_cdk import CfnOutput


class HushApiLambdaStack(Stack):
    def __init__(self, scope: Construct, id: str, cognito_stack: Stack, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Having same runtime for all lambdas makes deployment faster
        runtime_version = _lambda.Runtime.PYTHON_3_8
        lambdas_path = os.path.join("..", "backend", "lambda")

        lambda_function_hello = _lambda.Function(
            self,
            "HelloLambdaFunction",
            runtime=runtime_version,
            handler="lambda_hello.handler",
            code=_lambda.Code.from_asset(lambdas_path),
        )

        lambda_function_hello_authenticated = _lambda.Function(
            self, "AuthenticatedHelloLambdaFunction",
            runtime=runtime_version,
            handler="lambda_hello_authenticated.handler",
            code=_lambda.Code.from_asset(lambdas_path),
        )

        api = apigw.RestApi(
            self,
            "HushApi",
            rest_api_name="Hush API service",
            description="An API Gateway for the Hush service."
        )

        authorizer = apigw.CognitoUserPoolsAuthorizer(
            self,
            "HushAuthorizer",
            cognito_user_pools=[cognito_stack.user_pool]
        )

        v1_resource = api.root.add_resource("v1")  # Create the "v1" resource

        hello_resource = v1_resource.add_resource("hello")
        hello_resource.add_method(
            "GET",
            apigw.LambdaIntegration(lambda_function_hello)
        )

        hello_authenticated_resource = api.root.add_resource("helloauthenticated")
        hello_authenticated_resource.add_method(
            "GET",
            apigw.LambdaIntegration(lambda_function_hello_authenticated),
            authorization_type=apigw.AuthorizationType.COGNITO,
            authorizer=authorizer
        )
