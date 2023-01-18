#!/usr/bin/env python3

from aws_cdk import core
from vpc.cdk_vpc_stack import CdkVpcStack
from mwaa.mwaa_stack import MwaaStack


app = core.App()
vpc_stack = CdkVpcStack(app, 'VPC-Stack')
airflow_stack = MwaaStack(app, "mwaa",vpc=vpc_stack.vpc)

app.synth()
