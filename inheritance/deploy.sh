#!/usr/bin/env bash
AWS_REGION=$1

export PARAM1="param1"
export AWS_DEFAULT_REGION=$AWS_REGION

cdk synth
cdk diff