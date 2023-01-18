
from aws_cdk import core, aws_iam
from aws_cdk.core import SecretValue
from aws_cdk.aws_codecommit import IRepository
from aws_cdk.aws_codecommit import Repository
from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as cpactions
from aws_cdk import pipelines
from aws_cdk import aws_codebuild
from aws_cdk import aws_iam as iam
from .appdeploy import AppDeploy


class PipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, config:dict = None,**kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        accounts = config.get("accounts")
        region: str = accounts["dev"]["region"]        
        dev_account: str = accounts["dev"]["account"]

        source_artifact = codepipeline.Artifact()
        caa = codepipeline.Artifact() 
        secret =  SecretValue("unw/mysecret")
        repo = Repository(self,"ungerw1",repository_name="ungerw1")

        pipeline = pipelines.CdkPipeline(self, 
                                         "unw-pipeline",
                                         cloud_assembly_artifact=caa,
                                         pipeline_name="unw-pipeline",
                                         source_action=cpactions.CodeCommitSourceAction(
                                             action_name='CodeCommit',
                                             repository=repo,
                                             branch=config["development_branch"],
                                             output=source_artifact,),

                                        #  source_action=cpactions.GitHubSourceAction (
                                        #      action_name='GitHub',
                                        #      oauth_token=secret,
                                        #      owner='ungerw',
                                        #      repo='test-repo',
                                        #      branch=config["main"],
                                        #      output=source_artifact,),

                                        #  source_action=cpactions.CodeStarConnectionsSourceAction(
                                        #      action_name='GitHub',
                                        #      connection_arn=codestar_connection_arn,
                                        #      owner='ungerw',
                                        #      repo='test-repo',
                                        #      branch=config["development_branch"],
                                        #      trigger_on_push=True,
                                        #      output=source_artifact,),

                                         synth_action=pipelines.SimpleSynthAction.standard_npm_synth(
                                             source_artifact=source_artifact,
                                             cloud_assembly_artifact=caa,
                                             install_command="npm install -g aws-cdk && pip install -r requirements.txt",
                                             environment=aws_codebuild.BuildEnvironment(
                                                 build_image=aws_codebuild.LinuxBuildImage.STANDARD_5_0,
                                                 privileged=True
                                             ),
                                             build_command='cdk list',
                                             synth_command='cdk synth',
                                         ))     

        dev_app = AppDeploy(self, 'dev', config=config, env={
            'account': dev_account,
            'region': region,
        })
        dev_stage = pipeline.add_application_stage(dev_app)
    
        dev_stage.add_actions(pipelines.ShellScriptAction(
            action_name='UnitTests',
            run_order=dev_stage.next_sequential_run_order(),
            additional_artifacts=[source_artifact],
            commands=[
                'pip install -r requirements.txt',
                'pip install -r requirements_dev.txt',
            ]))        
                                     

