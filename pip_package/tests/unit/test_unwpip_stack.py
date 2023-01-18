import json
import pytest

from aws_cdk import core
from unwpip.unwpip_stack import UnwpipStack


def get_template():
    app = core.App()
    UnwpipStack(app, "unwpip")
    return json.dumps(app.synth().get_stack("unwpip").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
