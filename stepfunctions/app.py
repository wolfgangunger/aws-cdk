#!/usr/bin/env python3

from aws_cdk import core
from stepfunctions.stepfunctions_stack import StepFunctionStack
from lambdas.lambda_stack import LambdaStack

app = core.App()

lambda_stack = LambdaStack(app,"LambdaStack") 
StepFunctionStack(app, "Step-Functions-Stack", status_lambda=lambda_stack.status_lambda,submit_lambda=lambda_stack.submit_lambda )
app.synth()
