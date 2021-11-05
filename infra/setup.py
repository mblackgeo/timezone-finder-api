import setuptools

with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="tzapi-infra",
    version="0.1.0",
    description="CDK infra for the TimezoneFinder API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Martin Black",
    package_dir={"": "stacks"},
    packages=setuptools.find_packages(where="infra"),
    install_requires=[
        "aws-cdk.core==1.130.0",
        "aws-cdk.aws_iam==1.130.0",
        "aws-cdk.aws_sqs==1.130.0",
        "aws-cdk.aws_sns==1.130.0",
        "aws-cdk.aws_sns_subscriptions==1.130.0",
        "aws-cdk.aws_s3==1.130.0",
        "aws-cdk.aws_s3_notifications==1.130.0",
        "aws-cdk.aws_lambda==1.130.0",
        "aws-cdk.aws_lambda_event_sources==1.130.0",
        "aws-cdk.aws_ecr==1.130.0",
        "aws-cdk.aws_ecs==1.130.0",
        "aws-cdk.aws_ec2==1.130.0",
        "aws-cdk.aws_ssm==1.130.0",
        "aws-cdk.aws_codepipeline==1.130.0",
        "aws-cdk.aws_codepipeline_actions==1.130.0",
        "aws-cdk.aws_cloudwatch==1.130.0",
        "aws-cdk.aws_cloudwatch_actions==1.130.0",
        "aws-cdk.aws_codebuild==1.130.0",
        "aws-cdk.aws_events_targets==1.130.0",
        "aws-cdk.aws_events==1.130.0",
        "aws-cdk.aws_events_targets==1.130.0",
        "aws-cdk.aws_ecs_patterns==1.130.0",
        "python-dotenv~=0.17",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
)
