from aws_cdk import core
from aws_cdk.core import DefaultStackSynthesizer


from vpc.vpc_stack import VpcStack
from iam.iam_stack import IamStack

class AppDeploy(core.Stage):
    def __init__(self, scope: core.Construct, id: str, config: dict = None, **kwargs):
        super().__init__(scope, id, **kwargs)

        # put stage id into configuration object
        config["stage"] = id

        #iam = IamStack(self, "unw-iam-stack", config=config,synthesizer=DefaultStackSynthesizer())
        iam = IamStack(self, "unw-iam-stack", config=config)        
        vpc = VpcStack(self, "unw-vpc-stack",config=config)

        
