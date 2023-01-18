from aws_cdk import (
    aws_batch,
    aws_ec2,
    aws_ssm,
    core,
)

USR_DATA_STR = """MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="==MYBOUNDARY=="

--==MYBOUNDARY==
Content-Type: text/x-shellscript; charset="us-ascii"

#!/bin/bash
# only a dummy usr data script for this tutorial : Install Apache Web Server and PHP 
yum install -y httpd mysql 
amazon-linux-extras install -y php7.2 
# Download Lab files 
wget https://us-west-2-tcprod.s3.amazonaws.com/courses/ILT-TF-200-ARCHIT/v6.8.2/lab-2-webapp/scripts/inventory-app.zip 
unzip inventory-app.zip -d /var/www/html/ 
# Download and install the AWS SDK for PHP 
wget https://github.com/aws/aws-sdk-php/releases/download/3.62.3/aws.zip 
unzip aws -d /var/www/html 
# Turn on web server 
chkconfig httpd on 
service httpd start


--==MYBOUNDARY==--
"""


class BatchEc2ComputeConstruct(core.Construct):
    def __init__(
            self,
            scope: core.Construct,
            id: str,
            vpc,
            **kwargs,
    ) -> None:

        super().__init__(scope, id, **kwargs)
        #super().__init__(scope, id)

        self.vpc = vpc
        list_subnets = list(map(lambda x: x.subnet_id, self.vpc.private_subnets))


        self.sg_id = "sg-my-sg-id"

        launch_template_data = aws_ec2.CfnLaunchTemplate.LaunchTemplateDataProperty(
            user_data=core.Fn.base64(USR_DATA_STR),
            monitoring=aws_ec2.CfnLaunchTemplate.MonitoringProperty(
                enabled=True
            )
        )

        launch_template = aws_ec2.CfnLaunchTemplate(
            self, f"ec2-launch-template", launch_template_data=launch_template_data,
        )

        launch_template_props = aws_batch.CfnComputeEnvironment.LaunchTemplateSpecificationProperty(
            launch_template_id=launch_template.ref
        )

        self.compute_environmet = aws_batch.CfnComputeEnvironment(
            self,
            id=id,
            type="MANAGED",
            compute_resources=aws_batch.CfnComputeEnvironment.ComputeResourcesProperty(
                type="EC2",
                allocation_strategy="BEST_FIT_PROGRESSIVE",
                ec2_configuration=[aws_batch.CfnComputeEnvironment.Ec2ConfigurationObjectProperty(
                    image_type='ECS_AL2',
                )],
                instance_types=['m5d', 'm5ad', 'c5d', 'r5d'],
                launch_template=launch_template_props,
                maxv_cpus=8,
                minv_cpus=2,
                subnets=list_subnets,
                security_group_ids=[self.sg_id]
            ),
            state="ENABLED"
        )
        # Create Job Queue
        self.job_queue = aws_batch.CfnJobQueue(
            self,
            id="batch-job-queue",
            compute_environment_order=[aws_batch.CfnJobQueue.ComputeEnvironmentOrderProperty(
                compute_environment=self.compute_environmet.ref,
                order=1
            )],
            priority=1,
            job_queue_name=f'{id}-job-queue'
        )

