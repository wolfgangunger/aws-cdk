import json
import pytest

from aws_cdk import core
from ssm.ssm_stack import SsmStack


def get_template():
    app = core.App()
    SsmStack(app, "ssm")
    return json.dumps(app.synth().get_stack("ssm").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
