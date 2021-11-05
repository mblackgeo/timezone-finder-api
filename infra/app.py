from aws_cdk import core

from stacks.cicd_stack import CiCdStack
from stacks.config import conf
from stacks.networking_stack import NetworkingStack
from stacks.serving_stack import ServingStack

app = core.App()


cdk_environment = core.Environment(region=conf.aws_region, account=conf.aws_account)

cicd = CiCdStack(scope=app, id="cicd-stack", env=cdk_environment)

networking = NetworkingStack(app, "networking-stack", env=cdk_environment)

serving = ServingStack(
    app,
    id="serving-stack",
    vpc=networking.vpc,
    repository=cicd.ecr_repository,
    env=cdk_environment,
)

app.synth()
