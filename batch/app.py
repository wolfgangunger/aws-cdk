#!/usr/bin/env python3

from aws_cdk import core
from vpc.cdk_vpc_stack import CdkVpcStack
from batch.batch_stack import BatchStack


app = core.App()
vpc_stack = CdkVpcStack(app, 'VPC-Stack')
batch_stack = BatchStack(app, "Batch-Stack",vpc=vpc_stack.vpc)


app.synth()
