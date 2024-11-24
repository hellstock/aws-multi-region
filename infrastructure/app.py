from aws_cdk import App
from hush_cognito_stack import HushCognitoStack
from hush_api_lambda_stack import HushApiLambdaStack

app = App()
cognito_stack = HushCognitoStack(app, "HushCognitoStack")
HushApiLambdaStack(app, "HushApiLambdaStack", cognito_stack=cognito_stack)
app.synth()
