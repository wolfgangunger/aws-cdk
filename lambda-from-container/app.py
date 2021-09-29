
from aws_cdk import (
    core
)
from lambdas.lambda_stack import LambdaStack


class LambdaContainerFunctionStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

app = core.App()
env = {'region': 'eu-west-2'}
LambdaStack(app, "LambdaContainerFunctionStack", env=env)
app.synth()

