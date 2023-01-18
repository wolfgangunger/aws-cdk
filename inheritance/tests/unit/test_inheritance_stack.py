import json
import pytest

from aws_cdk import core
from inheritance.inheritance_stack import InheritanceStack


def get_template():
    app = core.App()
    InheritanceStack(app, "inheritance")
    return json.dumps(app.synth().get_stack("inheritance").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
