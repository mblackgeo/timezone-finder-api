from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as targets
from aws_cdk import core

from stacks.config import conf


class RestfulApiGatewayStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Configuration
        opts = apigw.StageOptions(stage_name="prod")

        # Setup Route 53 domain and certs if required
        if conf.domain_name:
            root_domain = conf.domain_name
            api_domain = f"{conf.api_subdomain}.{root_domain}"

            # Get the HostedZone of the root domain
            zone = route53.HostedZone.from_lookup(self, "baseZone", domain_name=root_domain)

            # Create a certificate for the api subdomain
            cert = acm.Certificate(
                self,
                "Certificate",
                domain_name=api_domain,
                validation=acm.CertificateValidation.from_dns(zone),
            )

            # Configure the api domain options for the rest api
            domain_opts = apigw.DomainNameOptions(certificate=cert, domain_name=api_domain)

            # Setting the STAGE env var for the lambda image is not required
            # when using a custom domain as the docs are served from the root path
            lambda_env = None

        else:
            # If we aren't using a custom domain we must set STAGE environment
            # variable so that the swagger api docs are served at the correct
            # path: i.e.: https://asd123.execute-api.eu-west-1.amazonaws.com/<STAGE_NAME>/
            lambda_env = {"STAGE": opts.stage_name}
            domain_opts = None

        # Register and build an Lambda docker image
        # This picks up on Dockerfile in the parent folder
        fn = _lambda.DockerImageFunction(
            self,
            "RestfulApiFxn",
            code=_lambda.DockerImageCode.from_image_asset(".."),
            environment=lambda_env,
        )

        # Create a Lambda based rest API with optional domain name
        api = apigw.LambdaRestApi(
            self,
            "TestRoute",
            handler=fn,
            deploy_options=opts,
            domain_name=domain_opts,
        )

        # Register the A record for the api if required
        if domain_opts is not None:
            route53.ARecord(
                self,
                "AliasRecord",
                record_name=api_domain,
                zone=zone,
                target=route53.RecordTarget.from_alias(targets.ApiGateway(api)),
            )
