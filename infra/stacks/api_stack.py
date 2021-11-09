from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_lambda as _lambda
from aws_cdk import core


class RestfulApiGatewayStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        opts = apigw.StageOptions(stage_name="prod")

        fn = _lambda.DockerImageFunction(
            self,
            "RestfulApiFxn",
            code=_lambda.DockerImageCode.from_image_asset(".."),
            environment={"STAGE": opts.stage_name},
        )

        api = apigw.LambdaRestApi(  # noqa: F841
            self,
            "TestRoute",
            handler=fn,
            deploy_options=opts,
        )
