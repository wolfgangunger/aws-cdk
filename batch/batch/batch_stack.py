from aws_cdk import (
    aws_batch,
    aws_ec2,
    aws_ssm,
    core,
)


from batch.batch_ec2_construct import BatchEc2ComputeConstruct
from batch.batch_fargate_construct import BatchFargateComputeConstruct

class BatchStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        batchConstructEc2 = BatchEc2ComputeConstruct(self, 'b-ec2', 
                                vpc=vpc)

        batchConstructFargate =  BatchFargateComputeConstruct(self, 'b-fargate', compenvtype="FARGATE",
                                 maxcpu=8, vpc=vpc)         
