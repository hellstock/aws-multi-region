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
    def __init__(self, scope: Construct, id: str, cognito_stack: Stack, dynamo_stack: Stack, **kwargs) -> None:
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

        lambda_function_store_match =  _lambda.Function(
            self, "TournamentStoreMatch",
            runtime=runtime_version,
            handler="lambda_match_store.handler",
            code=_lambda.Code.from_asset(lambdas_path),
        )
        lambda_function_store_match.add_environment(
            "DYNAMO_TABLE_NAME", dynamo_stack.table.table_name)
        dynamo_stack.table.grant_read_write_data(lambda_function_store_match)

        lambda_function_tournament_results = _lambda.Function(
            self, "TournamentGetResults",
            runtime=runtime_version,
            handler="lambda_tournament_get_results.handler",
            code=_lambda.Code.from_asset(lambdas_path),
        )
        lambda_function_tournament_results.add_environment(
            "DYNAMO_TABLE_NAME", dynamo_stack.table.table_name)

        dynamo_stack.table.grant_read_data(lambda_function_tournament_results)

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

        hello_authenticated_resource = v1_resource.add_resource("helloauthenticated")
        hello_authenticated_resource.add_method(
            "GET",
            apigw.LambdaIntegration(lambda_function_hello_authenticated),
            authorization_type=apigw.AuthorizationType.COGNITO,
            authorizer=authorizer
        )

        tournaments_resource = v1_resource.add_resource("tournament")

        match_post_resource = tournaments_resource.add_resource("match")
        match_post_resource.add_method(
            "POST",
            apigw.LambdaIntegration(lambda_function_store_match),
            authorization_type=apigw.AuthorizationType.COGNITO,
            authorizer=authorizer
        )

        tournament_resource = tournaments_resource.add_resource("{tournamentId}")
        results_resource = tournament_resource.add_resource("results")
        results_resource.add_method(
            "GET",
            apigw.LambdaIntegration(lambda_function_tournament_results)
        )
