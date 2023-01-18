#!/usr/bin/env python3

from aws_cdk import core

from iam.iam_stack import IamStack


app = core.App()
iam = IamStack(app, "iam")

app.synth()
