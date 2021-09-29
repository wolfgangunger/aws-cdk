from aws_cdk import core

from vpc.cdk_vpc_stack import CdkVpcStack
from ec2.ec2_stack import Ec2Stack


app = core.App()

vpc_stack = CdkVpcStack(app, 'VPC-Stack')
ec2_stack = Ec2Stack(app, "EC2-Stack", vpc=vpc_stack.vpc)

app.synth()
