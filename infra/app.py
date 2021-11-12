#!/usr/bin/env python3

from aws_cdk import core

from stacks.apiv2_stack import RestfulApiGatewayv2Stack
from stacks.config import conf

app = core.App()
cdk_env = core.Environment(region=conf.aws_region, account=conf.aws_account)

# Using API gateway v1
# from stacks.api_stack import RestfulApiGatewayStack
# RestfulApiGatewayStack(app, "tzfinder-api-stack", env=cdk_env)

# Using API gateway v2
# Note that domain name is required at the moment for this stack
RestfulApiGatewayv2Stack(app, "tzfinder-api-stack", env=cdk_env)

app.synth()
