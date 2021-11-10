import os
from types import SimpleNamespace

from dotenv import load_dotenv

# Load variables from .env
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))


conf = SimpleNamespace(
    aws_region=os.environ["AWS_REGION"],
    aws_account=os.environ["AWS_ACCOUNT"],
    domain_name=os.environ.get("DOMAIN_NAME", ""),
    api_subdomain=os.environ.get("API_SUBDOMAIN", ""),
)
