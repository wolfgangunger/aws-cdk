
from aws_cdk import core
import aws_cdk.aws_ec2 as ec2


class VpcConstruct(core.Construct):
    def __init__(
            self,
            scope: core.Construct,
            id: str,
            **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = ec2.Vpc(self, "VPC-CDK",
                        max_azs=3,
                        cidr="10.42.0.0/16",
                        subnet_configuration=[ec2.SubnetConfiguration(
                        subnet_type=ec2.SubnetType.PUBLIC,
                        name="Public",
                        cidr_mask=24
                        ), ec2.SubnetConfiguration(
                        subnet_type=ec2.SubnetType.PRIVATE,
                        name="Private",
                        cidr_mask=24
                        )
                        ],
                        nat_gateways=1,
                        )