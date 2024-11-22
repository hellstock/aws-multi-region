import os

from aws_cdk import (
    Aspects,
    IAspect,
    Stack,
    aws_logs as logs,
    aws_lambda as _lambda,
    aws_apigateway as apigw
)
from constructs import Construct
import jsii

@jsii.implements(IAspect)
class LogRetentionAspect:
    def __init__(self, retention: logs.RetentionDays):
        self.retention = retention

    def visit(self, node: Construct):
        if isinstance(node, logs.CfnLogGroup):
            node.add_property_override("RetentionInDays", self.retention.value)


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

        api = apigw.RestApi(
            self,
            "HushApi",
            rest_api_name="Hush API service",
            description="An API Gateway for the Hush service."
        )

        hello_resource = api.root.add_resource("hello")

        hello_resource.add_method(
            "GET",
            apigw.LambdaIntegration(lambda_function)
        )

        Aspects.of(self).add(LogRetentionAspect(logs.RetentionDays.ONE_MONTH))
