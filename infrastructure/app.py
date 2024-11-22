from aws_cdk import App
from hush_api_lambda_stack import HushApiLambdaStack

app = App()
HushApiLambdaStack(app, "HushApiLambdaStack")
app.synth()
