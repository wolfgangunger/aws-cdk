from aws_cdk import (
    aws_autoscaling as autoscaling,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    core,
)


class ECSCluster(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, *kwargs)


        asg = autoscaling.AutoScalingGroup(
            self, "MyFleet",
            instance_type=ec2.InstanceType("t2.xlarge"),
            machine_image=ecs.EcsOptimizedAmi(),
            associate_public_ip_address=True,
            update_type=autoscaling.UpdateType.REPLACING_UPDATE,
            desired_capacity=3,
            vpc=vpc,
            vpc_subnets={ 'subnet_type': ec2.SubnetType.PUBLIC },
        )

        self.cluster = ecs.Cluster(
            self, 'EcsCluster',
            vpc=vpc
        )

        self.cluster.add_auto_scaling_group(asg)
        self.cluster.add_capacity("DefaultAutoScalingGroup",
                             instance_type=ec2.InstanceType("t2.micro"))

        core.CfnOutput(
            self, "Cluster",
            value=self.cluster.cluster_name
        )