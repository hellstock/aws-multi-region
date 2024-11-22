import os

from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw
)
from constructs import Construct
from aws_cdk import CfnOutput


class HushApiLambdaStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        lambda_function = _lambda.Function(
            self,
            "HelloLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="lambda_hello.handler",
            code=_lambda.Code.from_asset(os.path.join("..", "backend", "lambda")),
        )

        api = apigw.LambdaRestApi(
            self,
            "HushApiGateway",
            handler=lambda_function,
            proxy=True
        )

        # Output the API Gateway endpoint URL
        CfnOutput(
            self,
            "ApiEndpoint",
            value=api.url,
            description="The API Gateway endpoint for the Lambda function"
        )
