#!/usr/bin/env python3

from aws_cdk import core as cdk
from hush_api_lambda_stack import HushApiLambdaStack

app = cdk.App()
HushApiLambdaStack(app, "HushApiLambdaStack")
app.synth()
