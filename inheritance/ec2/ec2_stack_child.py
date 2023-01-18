import os.path

from aws_cdk.aws_s3_assets import Asset
from ec2.ec2_construct import Ec2Construct
from ec2.ec2_stack import Ec2Stack

from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    core    
)



class Ec2StackChild(Ec2Stack):

    def __init__(self, scope: core.Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, vpc, **kwargs)

        core.CfnOutput(
            self, "EC2-public-IP-Child",
            value=self.ec2_construct.instance.instance_public_ip
        )
