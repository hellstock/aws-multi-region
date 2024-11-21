from aws_cdk import (
    core as cdk,
    aws_lambda as _lambda,
    aws_apigateway as apigw
)

class HushApiLambdaStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        lambda_function = _lambda.Function(
            self,
            "HelloLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="lambda_function.handler",
            code=_lambda.Code.from_asset("lambda"),
        )

        api = apigw.LambdaRestApi(
            self,
            "HushApiGateway",
            handler=lambda_function,
            proxy=True
        )

        # Output the API Gateway endpoint URL
        cdk.CfnOutput(
            self,
            "ApiEndpoint",
            value=api.url,
            description="The API Gateway endpoint for the Lambda function"
        )
