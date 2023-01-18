import json
import pytest

from aws_cdk import core
from efs.efs_stack import EfsStack


def get_template():
    app = core.App()
    EfsStack(app, "efs")
    return json.dumps(app.synth().get_stack("efs").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
