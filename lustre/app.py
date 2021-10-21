#!/usr/bin/env python3

from aws_cdk import core

from lustre.lustre_stack import LustreStack


app = core.App()
LustreStack(app, "lustre")

app.synth()
