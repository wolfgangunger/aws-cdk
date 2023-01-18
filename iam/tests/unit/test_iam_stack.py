import json
import pytest

from aws_cdk import core
from iam.iam_stack import IamStack


def get_template():
    app = core.App()
    IamStack(app, "iam")
    return json.dumps(app.synth().get_stack("iam").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
