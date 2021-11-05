
# TimezoneFinder API Infrastructure as code

## Overview

This CDK project follows the same approach as this post[^1], where the setup is as follows:

* CodePipeline clones the Github repository, builds a docker image for the app and uploads it to the Elastic Container Registry (ECR).
* An Elastic Container Service (ECS) cluster downloads the image from ECR and runs it in a container via Fargate.
* The cluster runs our app in a Virtual Private Cloud (VPC) and exposes it to the internet via a Load balancer.

As the code itself lives outside of AWS (i.e. here on Github), a connection should be made using the [AWS Console](https://console.aws.amazon.com/codesuite/settings/connections) so that AWS can clone the repository from Github.

## Development

This project was created with AWS CDK. The `cdk.json` file tells the CDK Toolkit how to execute your app.

A new virtual environment should be created for the infra deployment:

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Configuration is handled through the `.env` file. A copy of the `.env.example` file should be created and populated. It is also assumed that you AWS credentials are setup to work with  CDK and your AWS account has already been bootstrap for CDK (`cdk boostrap`).

At this point you can now synthesize the CloudFormation template for this code.

```shell
cdk synth
```

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation


[^1]: https://medium.com/axel-springer-tech/how-to-automatically-deploy-a-ml-classifier-to-the-cloud-with-aws-cdk-20f8946d913c