#!/usr/bin/env python3

from aws_cdk import core

from vpc.cdk_vpc_stack import CdkVpcStack
from ssm.ssm_stack import SsmStack


app = core.App()
vpc_stack = CdkVpcStack(app, 'VPC-Stack')
ssm_stack = SsmStack(app, "ssm",vpc=vpc_stack.vpc)

app.synth()
