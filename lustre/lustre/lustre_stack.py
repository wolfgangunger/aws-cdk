from aws_cdk import (
    aws_iam as iam,
    core,
    aws_ec2 as ec2,
    aws_fsx as fsx,
)



class LustreStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, "VPC-CDK",
                           max_azs=3,
                           cidr="10.43.0.0/16",
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
        
        file_system = fsx.LustreFileSystem(self, "FsxLustreFileSystem",
        lustre_configuration={"deployment_type": fsx.LustreDeploymentType.SCRATCH_2},
        storage_capacity_gib=1200,
        vpc=vpc,
        vpc_subnet=vpc.private_subnets[0]
        )
        ##
        inst = ec2.Instance(self, "inst",
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.LARGE),
            machine_image=ec2.AmazonLinuxImage(
                generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2
            ),
            vpc=vpc,
            vpc_subnets={
                "subnet_type": ec2.SubnetType.PUBLIC
            }
        )
        file_system.connections.allow_default_port_from(inst)

        # Need to give the instance access to read information about FSx to determine the file system's mount name.
        inst.role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonFSxReadOnlyAccess"))

        mount_path = "/mnt/fsx"
        dns_name = file_system.dns_name
        mount_name = file_system.mount_name

        #inst.user_data.add_commands("set -eux", "yum update -y", "amazon-linux-extras install -y lustre2.10", f"mkdir -p {mount_path}", f"chmod 777 {mount_path}", f"chown ec2-user:ec2-user {mount_path}", f"echo {dns_name}@tcp:/{mount_name} {mount_path} lustre defaults,noatime,flock,_netdev 0 0" >> /etc/fstab", "mount -a")        
        inst.user_data.add_commands("set -eux", "yum update -y", "amazon-linux-extras install -y lustre2.10", f"mkdir -p {mount_path}", f"chmod 777 {mount_path}", f"chown ec2-user:ec2-user {mount_path}", f"echo {dns_name}@tcp:/{mount_name} {mount_path} lustre defaults,noatime,flock,_netdev 0 0" )

