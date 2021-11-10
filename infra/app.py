#!/usr/bin/env python3

from aws_cdk import core

from stacks.api_stack import RestfulApiGatewayStack
from stacks.config import conf

app = core.App()
cdk_env = core.Environment(region=conf.aws_region, account=conf.aws_account)

RestfulApiGatewayStack(app, "restful-api-gateway-stack", env=cdk_env)

app.synth()
