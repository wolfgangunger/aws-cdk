import os.path

from aws_cdk.aws_s3_assets import Asset
from ec2.ec2_construct import Ec2Construct

from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    core    
)



class Ec2Stack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        self.ec2_construct = Ec2Construct(self, "ec2-construct",vpc)


        core.CfnOutput(
            self, "EC2-Super",
            value=self.ec2_construct.instance.instance_id
        )
        core.CfnOutput(
            self, "EC2-private-IP-Super",
            value=self.ec2_construct.instance.instance_private_ip
        )
