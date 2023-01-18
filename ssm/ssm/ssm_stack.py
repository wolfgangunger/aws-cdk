from aws_cdk import (
    aws_ec2,
    aws_ssm,
    core
)


class SsmStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = vpc
        # Creates SSM Parameters to store default sg id
        aws_ssm.StringParameter(
            self, 
            "ssm-param1",
            parameter_name="key1",
            string_value="value1"
        )
        
        # Creates SSM Parameters to store vpc sg id
        aws_ssm.StringParameter(
            self, 
            "ssm-param2",
            parameter_name="vpc-id",
            string_value=self.vpc.vpc_id
        )
