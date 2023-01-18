from aws_cdk import (
    aws_ec2 as ec2,
    aws_rds,
    core,
)


class RdsStackPostgres(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        self.subnet_grp_name = aws_rds.SubnetGroup(
            self,
            id=f'{id}-db-subnet-group',
            vpc=vpc,
            subnet_group_name=f'{id}-db_subnet_group',
            description='DB Subnet group'
        )

        self.postgres = aws_rds.DatabaseInstance(
            self,
            id=f'{id}-postgres-db-instance',
            credentials=aws_rds.Credentials.from_generated_secret(
                username='postgres',
                secret_name=f'my-secret'
            ),
            storage_encrypted=True,
            engine=aws_rds.DatabaseInstanceEngine.postgres(version=aws_rds.PostgresEngineVersion.VER_13_2),
            allocated_storage=1000,
            instance_identifier=f'{id}-postgres-db-instance',
            database_name='postgres',
            instance_type=ec2.InstanceType('m6g.large'),
            backup_retention=core.Duration.days(0),
            parameter_group=aws_rds.ParameterGroup.from_parameter_group_name(
                self,
                id="param-grp",
                parameter_group_name='default.postgres13'
            ),
            vpc=vpc,
            multi_az=True,
            publicly_accessible=False,
            #security_groups=[auth.default_sg, auth.vpc_sg, auth.postgres_sg],
            subnet_group=self.subnet_grp_name
        )

