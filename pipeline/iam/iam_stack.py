from aws_cdk import (
    aws_iam,
    core
)


class IamStack(core.Stack):

    def __init__(self, 
                scope: core.Construct, 
                construct_id: str,
                config:dict,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        self.role_policy = aws_iam.PolicyDocument(
            statements=[
                aws_iam.PolicyStatement(
                    actions=[
                        "ec2:StartInstances",
                        "ec2:StopInstances"
                    ],
                    effect=aws_iam.Effect.ALLOW,
                    resources=["*"],
                )
           ]
        )

        self.kms_policy_document = aws_iam.PolicyDocument(
            statements=[
                aws_iam.PolicyStatement(
                    actions=[
                        "kms:*"
                    ],
                    effect=aws_iam.Effect.ALLOW,
                    resources=["*"],
                )
            ]
        )    

        self.job_role=aws_iam.Role(
            self,
            id='ecs-job-role',
            assumed_by=aws_iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
            role_name=f'{id}-ecs-job-role',
            description ='Allows ECS tasks to call AWS services on your behalf',
            managed_policies=[
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonRDSFullAccess'),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('SecretsManagerReadWrite'),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchLogsFullAccess'),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AmazonECSTaskExecutionRolePolicy')
            ],
            inline_policies={"KMSPolicyDocument": self.kms_policy_document, "RolePolicyDocument": self.role_policy}
        )            