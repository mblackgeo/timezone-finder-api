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
        root_domain = conf.domain_name
        api_domain = f"api.{root_domain}"

        # Register and build an Lambda docker image
        # This picks up on Dockerfile in the parent folder
        fn = _lambda.DockerImageFunction(
            self,
            "RestfulApiFxn",
            code=_lambda.DockerImageCode.from_image_asset(".."),
            environment={"STAGE": opts.stage_name},
        )

        # Setup the Route53 domain and certs
        zone = route53.HostedZone.from_lookup(self, "baseZone", domain_name=root_domain)
        cert = acm.Certificate(
            self,
            "Certificate",
            domain_name=api_domain,
            validation=acm.CertificateValidation.from_dns(zone),
        )

        # Create a Lambda based rest API
        api = apigw.LambdaRestApi(
            self,
            "TestRoute",
            handler=fn,
            deploy_options=opts,
            domain_name=apigw.DomainNameOptions(certificate=cert, domain_name=api_domain),
        )

        # Register the A record for the api
        route53.ARecord(self, "AliasRecord", zone=zone, target=route53.RecordTarget.from_alias(targets.ApiGateway(api)))
