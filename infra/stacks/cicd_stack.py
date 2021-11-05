from aws_cdk import aws_codebuild as build
from aws_cdk import aws_codepipeline as pipeline
from aws_cdk import aws_codepipeline_actions as actions
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3 as s3
from aws_cdk import core

from stacks.config import conf


class CiCdStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.pipeline_id = f"{id}-cicd-stack"

        # Create an S3 bucket that will hold the repository colned from Github
        artifact_bucket = s3.Bucket(
            scope=self,
            id=f"{id}-artifacts-bucket",
            removal_policy=core.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            encryption=s3.BucketEncryption.KMS_MANAGED,
            versioned=False,
            lifecycle_rules=[s3.LifecycleRule(expiration=core.Duration.days(2))],
        )

        # Create CodePipeline that will build the docker image
        build_pipeline = pipeline.Pipeline(
            scope=self,
            id=f"{id}-pipeline",
            artifact_bucket=artifact_bucket,
            pipeline_name=self.pipeline_id,
            restart_execution_on_update=True,
        )

        source_output = pipeline.Artifact()

        # Cloning from GH to S3
        build_pipeline.add_stage(
            stage_name="GithubSources",
            actions=[
                # Despite the action name, this does work with Github as well
                actions.BitBucketSourceAction(
                    connection_arn=conf.github_connection_arn,
                    owner=conf.github_owner,
                    repo=conf.github_repo,
                    action_name="SourceCodeRepo",
                    branch="master",
                    output=source_output,
                )
            ],
        )

        # Make an ECR repo to hold the built docker images
        self.ecr_repository = ecr.Repository(scope=self, id=f"{id}-ecr-repo")
        self.ecr_repository.add_lifecycle_rule(max_image_age=core.Duration.days(7))

        # Setup CodeBuild as part of the pipeline
        build_project = build.PipelineProject(
            scope=self,
            id=f"{id}-build-project",
            project_name="TimezoneFinderApiBuildProject",
            description="Build project for the TimezoneFinder Api",
            environment=build.BuildEnvironment(
                build_image=build.LinuxBuildImage.STANDARD_3_0, privileged=True, compute_type=build.ComputeType.SMALL
            ),
            environment_variables={
                "REPOSITORY_URI": build.BuildEnvironmentVariable(value=self.ecr_repository.repository_uri),
            },
            timeout=core.Duration.minutes(15),
            cache=build.Cache.bucket(artifact_bucket, prefix="codebuild-cache"),
            build_spec=build.BuildSpec.from_source_filename("buildspec.yml"),
        )

        build_project.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    "codebuild:CreateReportGroup",
                    "codebuild:CreateReport",
                    "codebuild:BatchPutTestCases",
                    "codebuild:UpdateReport",
                    "codebuild:StartBuild",
                ],
                resources=["*"],
            )
        )

        self.ecr_repository.grant_pull_push(build_project)

        build_output = pipeline.Artifact()

        # Build the container
        build_pipeline.add_stage(
            stage_name="BuildStage",
            actions=[
                actions.CodeBuildAction(
                    action_name="CodeBuildProjectAction",
                    input=source_output,
                    outputs=[build_output],
                    project=build_project,
                    type=actions.CodeBuildActionType.BUILD,
                    run_order=1,
                )
            ],
        )
