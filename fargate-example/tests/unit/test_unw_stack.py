import json
import pytest

from aws_cdk import core
from unw.unw_stack import UnwStack


def get_template():
    app = core.App()
    UnwStack(app, "unw")
    return json.dumps(app.synth().get_stack("unw").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
