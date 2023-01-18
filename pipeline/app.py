#!/usr/bin/env python3

from aws_cdk import core

from pipeline.pipeline_stack import PipelineStack

env_unw = core.Environment(account="039735417706", region="eu-central-1")

app = core.App()
config = app.node.try_get_context("config")
PipelineStack(app, "pipeline",config={**config},env=env_unw)

app.synth()
