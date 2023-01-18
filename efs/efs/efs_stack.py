from aws_cdk import (
    aws_efs,
    core
)


class EfsStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = vpc
        
        self.sg_id = "sg-my-sg-id"

        self.file_system = aws_efs.FileSystem(
            self,
            id="file-system",
            vpc=self.vpc,
            performance_mode=aws_efs.PerformanceMode("GENERAL_PURPOSE"),
            throughput_mode=aws_efs.ThroughputMode('BURSTING'),
            encrypted=True,
            file_system_name=f"{id}-file-system",
            lifecycle_policy=None
        )