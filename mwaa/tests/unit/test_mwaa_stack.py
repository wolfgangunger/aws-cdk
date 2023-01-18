import json
import pytest

from aws_cdk import core
from mwaa.mwaa_stack import MwaaStack


def get_template():
    app = core.App()
    MwaaStack(app, "mwaa")
    return json.dumps(app.synth().get_stack("mwaa").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
