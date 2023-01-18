from aws_cdk import (
    aws_ec2 as ec2,
    aws_s3,
    aws_iam,
    aws_mwaa,
    aws_s3_deployment,
    core,
    aws_ssm
)


class MwaaStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str,vpc,  **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = vpc
        list_subnets = list(map(lambda x: x.subnet_id, self.vpc.private_subnets))
        mwaa_subnet_ids = list_subnets[:-1]

        self.sg_id = "sg-my-sg-id"

        mwaa_network_configuration = aws_mwaa.CfnEnvironment.NetworkConfigurationProperty(
            security_group_ids=[self.sg_id],
            subnet_ids=mwaa_subnet_ids,
        )

        mwaa_policy_document = aws_iam.PolicyDocument(
            statements=[
                aws_iam.PolicyStatement(
                    actions=["airflow:PublishMetrics"],
                    effect=aws_iam.Effect.ALLOW,
                    resources=[f"arn:aws:airflow:{self.region}:{self.account}:environment/{id}-v2"],
                ),
                aws_iam.PolicyStatement(
                    actions=[
                        "logs:CreateLogStream",
                        "logs:CreateLogGroup",
                        "logs:PutLogEvents",
                        "logs:GetLogEvents",
                        "logs:GetLogRecord",
                        "logs:GetLogGroupFields",
                        "logs:GetQueryResults"
                    ],
                    effect=aws_iam.Effect.ALLOW,
                    resources=[
                        f"arn:aws:logs:{self.region}:{self.account}:log-group:airflow-{id}-v2-*"],
                ),
                aws_iam.PolicyStatement(
                    actions=[
                        "logs:DescribeLogGroups"
                    ],
                    effect=aws_iam.Effect.ALLOW,
                    resources=["*"],
                ),
                aws_iam.PolicyStatement(
                    actions=[
                        "cloudwatch:PutMetricData"
                    ],
                    effect=aws_iam.Effect.ALLOW,
                    resources=["*"],
                ),
                aws_iam.PolicyStatement(
                    # restrict actions for use case
                    actions=[
                        "ecs:*",
                        "s3:*",
                        "sqs:*",
                        "sns:*",
                        "dynamodb:*",
                        "ssm:*",
                        "logs:*",
                        "airflow:*",
                        "batch:*",
                        "iam:PassRole",
                        "kms:*"
                    ],
                    effect=aws_iam.Effect.ALLOW,
                    resources=["*"],
                )
            ]
        )


        mwaa_service_role = aws_iam.Role(
            self,
            "mwaa-service-role",
            assumed_by=aws_iam.CompositePrincipal(
                aws_iam.ServicePrincipal("airflow.amazonaws.com"),
                aws_iam.ServicePrincipal("airflow-env.amazonaws.com"),
            ),
            inline_policies={"CDKmwaaPolicyDocument": mwaa_policy_document},
            path="/service-role/"
        )

        mwaa_service_role.assume_role_policy.add_statements(
            aws_iam.PolicyStatement(
                actions=["sts:AssumeRole"],
                effect=aws_iam.Effect.ALLOW,
                principals=[aws_iam.ServicePrincipal("airflow-env.amazonaws.com")]
            )
        )

        mwaa_logging_conf = aws_mwaa.CfnEnvironment.LoggingConfigurationProperty(
            task_logs=aws_mwaa.CfnEnvironment.ModuleLoggingConfigurationProperty(enabled=True, log_level="INFO"),
            worker_logs=aws_mwaa.CfnEnvironment.ModuleLoggingConfigurationProperty(enabled=True, log_level="INFO"),
            scheduler_logs=aws_mwaa.CfnEnvironment.ModuleLoggingConfigurationProperty(enabled=True, log_level="INFO"),
            dag_processing_logs=aws_mwaa.CfnEnvironment.ModuleLoggingConfigurationProperty(enabled=True, log_level="INFO"),
            webserver_logs=aws_mwaa.CfnEnvironment.ModuleLoggingConfigurationProperty(enabled=True, log_level="INFO")
        )

        dag_bucket = aws_s3.Bucket(
            self,
            id="ungerw-airflow-bucket",
            bucket_name=f"airflow-dags-{self.stack_name}-{self.account}",
            removal_policy=core.RemovalPolicy.DESTROY,
            encryption=aws_s3.BucketEncryption.KMS_MANAGED,
            block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL
        )

        mwaa_environment_v2 = aws_mwaa.CfnEnvironment(
            self,
            id="mwaa-environment",
            airflow_version="2.0.2",
            dag_s3_path="dags",
            environment_class="mw1.medium",
            execution_role_arn=mwaa_service_role.role_arn,
            logging_configuration=mwaa_logging_conf,
            name=f"apache airflow example",
            network_configuration=mwaa_network_configuration,
            max_workers=3,
            plugins_s3_path="plugins/plugins.zip",
            requirements_s3_path="requirements/requirements.txt",
            source_bucket_arn=dag_bucket.bucket_arn,
            webserver_access_mode="PUBLIC_ONLY"
        )