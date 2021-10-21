from aws_cdk import core

from ec2.ec2_stack import Ec2Stack


app = core.App()

ec2_stack = Ec2Stack(app, "EC2-Stack")

app.synth()
