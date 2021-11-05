"""App configuration."""
import os
from types import SimpleNamespace

from dotenv import load_dotenv

# Load variables from .env
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))


conf = SimpleNamespace(
    aws_region=os.environ["AWS_REGION"],
    aws_account=os.environ["AWS_ACCOUNT"],
    github_connection_arn=os.environ["GITHUB_CONNECTION_ARN"],
    github_owner=os.environ["GITHUB_OWNER"],
    github_repo=os.environ["GITHUB_REPO"],
    fargate_memory_limit_mb=int(os.environ["FARGATE_MEMORY_LIMIT_MB"]),
    fargate_cpu_units=int(os.environ["FARGATE_CPU_UNITS"]),
    port=int(os.environ["PORT"]),
)
