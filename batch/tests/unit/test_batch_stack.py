import json
import pytest

from aws_cdk import core
from batch.batch_stack import BatchStack
from vpc.cdk_vpc_stack import CdkVpcStack


def get_template():
    app = core.App()
    vpc_stack = CdkVpcStack(app, 'VPC-Stack')
    BatchStack(app, "batch",vpc_stack.vpc)
    return json.dumps(app.synth().get_stack("batch").template)


def test_batch_queue_created():
    assert("AWS::Batch::JobQueue" in get_template())

def test_batch_env_created():
    assert("AWS::Batch::ComputeEnvironment" in get_template())


