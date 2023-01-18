from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
from vpc.vpc_construct import VpcConstruct


class CdkVpcStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
 
        self.vpc_construct = VpcConstruct(self,"vpc-standard")


        core.CfnOutput(self, "VPC-ID",
                       value=self.vpc_construct.vpc.vpc_id)
        core.CfnOutput(self, "CIDR",
                       value=self.vpc_construct.vpc.vpc_cidr_block)
