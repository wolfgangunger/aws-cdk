#!/usr/bin/env python3

from aws_cdk import core
from stepfunctions.stepfunctions_stack import JobPollerStack

app = core.App()
JobPollerStack(app, "Step-Functions-Stack")
app.synth()
