from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_patterns
from aws_cdk import aws_elasticloadbalancingv2 as elb
from aws_cdk import aws_logs as logs
from aws_cdk import core

from stacks.config import conf


class ServingStack(core.Stack):
    def __init__(
        self,
        scope: core.Construct,
        id: str,
        vpc: ec2.Vpc,
        repository: ecr.Repository,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = vpc

        self.ecs_cluster = ecs.Cluster(
            self, id=f"{id}-ecs", cluster_name="serving-ecs", vpc=self.vpc, container_insights=True
        )

        self.task_definition = ecs.FargateTaskDefinition(
            self,
            id=f"{id}-ecs-task-definition",
            memory_limit_mib=conf.fargate_memory_limit_mb,
            cpu=conf.fargate_cpu_units,
        )

        image = ecs.ContainerImage.from_ecr_repository(repository, "latest")

        log_driver = ecs.AwsLogDriver(stream_prefix=id, log_retention=logs.RetentionDays.ONE_DAY)

        app_container = self.task_definition.add_container(
            id=f"{id}-container",
            image=image,
            logging=log_driver,
        )

        app_container.add_port_mappings(ecs.PortMapping(container_port=conf.port, host_port=conf.port))

        self.service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            id=f"{id}-fargate-service",
            assign_public_ip=True,
            cluster=self.ecs_cluster,
            desired_count=1,
            task_definition=self.task_definition,
            open_listener=True,
            listener_port=conf.port,
            target_protocol=elb.ApplicationProtocol.HTTP,
        )
