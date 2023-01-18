#!/usr/bin/env python3

from aws_cdk import core

from efs.efs_stack import EfsStack
from vpc.cdk_vpc_stack import CdkVpcStack




app = core.App()
vpc_stack = CdkVpcStack(app, 'VPC-Stack')
efs_stack = EfsStack(app, "efs", vpc=vpc_stack.vpc)

app.synth()
