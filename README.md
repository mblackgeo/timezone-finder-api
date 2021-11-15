# timezone-finder-api
An API to quickly find the [timezone ID](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) of a point at a given latitude/longitude.

Built on:

* [FastAPI](https://fastapi.tiangolo.com)
* [timezonefinder](https://github.com/jannikmi/timezonefinder)
* `python>=3.7`

## Quick Guide

To get started quickly simply clone the repository and build and run:

```shell
make run-local
```

This will start a local instance of FastAPI which can then be queried with latitude and longitude to return a string of the timezone, for example:

```shell
make test-local

# Or curl directly:
curl -X POST "http://0.0.0.0:8000/tz-at/" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"lat\":0,\"lng\":0}"
```

The Swagger API documentation can reached at [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs).

## Development

To develop, set up a new clean virtual environment and install the requirements:

```shell
mkvirtualenv --python=/usr/bin/python3.7 tzapi
pip3 install -r requirements.txt
pip3 install -r requirements-dev.txt
pre-commit install
```

* [Pytest](https://docs.pytest.org/en/6.2.x/) is used for the functional tests of the application (see [`/tests`](tests/)).
* Code is linted using [flake8](https://flake8.pycqa.org/en/latest/) with `--max-line-length=120`
* Code formatting is validated using [Black](https://github.com/psf/black)
* [pre-commit](https://pre-commit.com/) is used to run these checks locally before files are pushed to git
* The [Github Actions pipeline](.github/workflows/pipeline.yml) also runs these checks and tests

## Deployment

Full deployment is handled by the [AWS CDK](https://aws.amazon.com/cdk/). See further details in [`/infra`](infra/).

This uses AWS Lambda and AWS API Gateway. A local version of the container that is used by AWS Lambda can be build/run/tested locally with the following commands:

```shell
make run-local-lambda
make test-local-lambda
```
