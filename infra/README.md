
# TimezoneFinder API Infrastructure as code

## Overview

This CDK project deploys the API using AWS Lambda and AWS API Gateway

## Development

This project was created with AWS CDK. The `cdk.json` file tells the CDK Toolkit how to execute your app.

A new virtual environment should be created for the infra deployment:

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# if this is the first time CDK has been used, your account should be bootstrapped
cdk bootstrap
```

CDK can then be used to deploy:

```shell
# synth the cloud formation template to ensure there are no errors
cdk synth

# deploy the api
cdk deploy

# To remove
# Note that CDK cannot yet remove the images stored in ECR so this should
# be done manually
cdk destroy
```

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation
