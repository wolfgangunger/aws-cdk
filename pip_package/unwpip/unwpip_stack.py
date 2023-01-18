from aws_cdk import (
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    core
)
import aws_cdk.aws_ec2 as ec2
#importing self created pip packages
from cdk_construct1.iam_construct import IAMConstructUnw
from cdk_construct1.batch_fargate_construct import BatchFargateComputeConstructUnw


class UnwpipStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)



        self.vpc = ec2.Vpc(self, "VPC-CDK",
                           max_azs=3,
                           cidr="10.42.0.0/16",
                           subnet_configuration=[ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PUBLIC,
                               name="Public",
                               cidr_mask=24
                           ), ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PRIVATE,
                               name="Private",
                               cidr_mask=24
                           )
                           ],
                           nat_gateways=1,
                           )

        ## using self created constructs with pip
        ## see https://pypi.org/project/cdk-construct1/
        batchConstructFargate =  BatchFargateComputeConstructUnw(self, 'b-fargate', compenvtype="FARGATE",
                                 maxcpu=8, vpc=self.vpc)      

        iamConstruct = IAMConstructUnw(self, "test-unw-constrcut")

