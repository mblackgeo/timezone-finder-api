from aws_cdk import aws_apigatewayv2 as apigw
from aws_cdk import aws_apigatewayv2_integrations as apigw_integrations
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as targets
from aws_cdk import core

from stacks.config import conf


class RestfulApiGatewayv2Stack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Setup Route 53 domain and certs
        # TODO make this optional
        root_domain = conf.domain_name
        api_domain = f"{conf.api_subdomain}.{root_domain}"

        # Get the HostedZone of the root domain
        zone = route53.HostedZone.from_lookup(
            scope=self,
            id=f"{id}-hosted-zone",
            domain_name=root_domain,
        )

        # Create a certificate for the api subdomain
        cert = acm.Certificate(
            scope=self,
            id=f"{id}-certificate",
            domain_name=api_domain,
            validation=acm.CertificateValidation.from_dns(zone),
        )

        # Configure the api domain options for the rest api
        domain_name = apigw.DomainName(scope=self, id=f"{id}-domain-name", certificate=cert, domain_name=api_domain)

        # Register and build an Lambda docker image
        # This picks up on Dockerfile in the parent folder
        fn = _lambda.DockerImageFunction(
            scope=self,
            id=f"{id}-restfulapifxn",
            code=_lambda.DockerImageCode.from_image_asset(directory="..", file="Dockerfile.aws"),
        )

        http_api = apigw.HttpApi(
            scope=self,
            id=f"{id}-endpoint",
            default_integration=apigw_integrations.LambdaProxyIntegration(handler=fn),
            default_domain_mapping=apigw.DomainMappingOptions(domain_name=domain_name),
        )

        http_api.add_routes(
            path="/",
            methods=[apigw.HttpMethod.ANY],
            integration=apigw_integrations.LambdaProxyIntegration(handler=fn),
        )

        # Register the A record for the api
        route53.ARecord(
            scope=self,
            id=f"{id}-aliasrecord",
            zone=zone,
            record_name=api_domain,
            target=route53.RecordTarget.from_alias(
                targets.ApiGatewayv2DomainProperties(
                    regional_domain_name=domain_name.regional_domain_name,
                    regional_hosted_zone_id=domain_name.regional_hosted_zone_id,
                )
            ),
        )
