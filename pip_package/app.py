#!/usr/bin/env python3

from aws_cdk import core

from unwpip.unwpip_stack import UnwpipStack


app = core.App()
UnwpipStack(app, "unwpip")

app.synth()
