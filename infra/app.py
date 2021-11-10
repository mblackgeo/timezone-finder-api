#!/usr/bin/env python3

from aws_cdk import core

from stacks.api_stack import RestfulApiGatewayStack

app = core.App()

RestfulApiGatewayStack(app, "restful-api-gateway-stack")

app.synth()
