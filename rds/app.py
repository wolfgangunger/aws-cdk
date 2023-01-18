#!/usr/bin/env python3

from aws_cdk import core

from vpc.cdk_vpc_stack import CdkVpcStack
from rds.rds_stack_mysql import RdsStackMySQL
from rds.rds_stack_postgres import RdsStackPostgres


app = core.App()

vpc_stack = CdkVpcStack(app, 'VPC-Stack')
rds_stack_mysql = RdsStackMySQL(app, "RDS-Stack-MySQL", vpc=vpc_stack.vpc)
rds_stack_postgres = RdsStackPostgres(app, "RDS-Stack-Postgres", vpc=vpc_stack.vpc)

app.synth()
