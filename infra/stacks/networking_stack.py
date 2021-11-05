from aws_cdk import aws_ec2 as ec2
from aws_cdk import core


class NetworkingStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = ec2.Vpc(scope=self, id=f"{id}-vpc", cidr="10.0.8.0/21")

        # S3 endpoint
        self.vpc_s3e = ec2.GatewayVpcEndpoint(
            scope=self,
            id=f"{id}-vpce-s3",
            vpc=self.vpc,
            service=ec2.GatewayVpcEndpointAwsService.S3,
            subnets=[ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE)],
        )
