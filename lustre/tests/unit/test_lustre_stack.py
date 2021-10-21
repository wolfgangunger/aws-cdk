import json
import pytest

from aws_cdk import core
from lustre.lustre_stack import LustreStack


def get_template():
    app = core.App()
    LustreStack(app, "lustre")
    return json.dumps(app.synth().get_stack("lustre").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
