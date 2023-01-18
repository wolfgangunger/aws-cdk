#!/usr/bin/env python3
import os
from aws_cdk import core

from inheritance.inheritance_stack import InheritanceStack
from vpc.vpc_stack import CdkVpcStack
from ec2.ec2_stack import Ec2Stack
from ec2.ec2_stack_child import Ec2StackChild


#region=os.environ["AWS_DEFAULT_REGION"]
#param1=os.environ["PARAM1"]
#print(region + " " + param1)

app = core.App()



#config = app.node.try_get_context("config")
#bucket_name = config.get("bucket_name")
bucket_name = app.node.try_get_context("bucket_name")
print(bucket_name)

vpc_stack = CdkVpcStack(app, 'VPC-Stack')
ec2_stack = Ec2Stack(app,"EC2-Stack", vpc_stack.vpc_construct.vpc)
ec2_stack_child = Ec2StackChild(app,"EC2-Stack-Child", vpc_stack.vpc_construct.vpc)

inh_stack = InheritanceStack(app, "inheritance")

app.synth()
