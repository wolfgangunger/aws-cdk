#!/usr/bin/env python3

from aws_cdk import core

from vpc.cdk_vpc_stack import CdkVpcStack
from rds.rds_stack import RdsStack


app = core.App()

vpc_stack = CdkVpcStack(app, 'VPC-Stack')
rds_stack = RdsStack(app, "RDS-Stack", vpc=vpc_stack.vpc)

app.synth()
