from aws_cdk import App
from hush_dynamo_stack import HushDynamoDbStack
from hush_cognito_stack import HushCognitoStack
from hush_api_lambda_stack import HushApiLambdaStack

app = App()
dynamo_stack=HushDynamoDbStack(app, "HushDynamoDbStack")
cognito_stack = HushCognitoStack(app, "HushCognitoStack")
HushApiLambdaStack(app, "HushApiLambdaStack", cognito_stack=cognito_stack, dynamo_stack=dynamo_stack)
app.synth()
