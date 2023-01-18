from aws_cdk import (
    aws_iam as iam,
    core
)
from vpc.vpc_stack import CdkVpcStack
from ec2.ec2_stack import Ec2Stack
from ec2.ec2_stack_child import Ec2StackChild


class InheritanceStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        vpc_stack = CdkVpcStack(self, 'VPC-Stack-2')
        ec2_stack = Ec2Stack(self,"EC2-Stack-2", vpc_stack.vpc_construct.vpc)  
        ec2_stack_child = Ec2StackChild(self,"EC2-Stack-Child-2", vpc_stack.vpc_construct.vpc)  