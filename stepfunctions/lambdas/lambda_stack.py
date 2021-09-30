from aws_cdk import (
    aws_lambda as _lambda,
    core,
)


class LambdaStack(core.Stack):
    def __init__(self, app: core.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        # Lambda Handlers Definitions

        self.submit_lambda = _lambda.Function(self, 'submitLambda',
                                         handler='lambda_function.lambda_handler',
                                         runtime=_lambda.Runtime.PYTHON_3_9,
                                         code=_lambda.Code.asset('lambdas/submit'))
        core.Tags.of(self.submit_lambda).add("Name", "Submit Lambda", priority=300)

        self.status_lambda = _lambda.Function(self, 'statusLambda',
                                         handler='lambda_function.lambda_handler',
                                         runtime=_lambda.Runtime.PYTHON_3_9,
                                         code=_lambda.Code.asset('lambdas/status'))
        core.Tags.of(self.status_lambda).add("Name", "Status Lambda", priority=300)


