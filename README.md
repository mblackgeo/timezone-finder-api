# timezone-finder-api
An API to quickly find the [timezone ID](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) of a point at a given latitude/longitude.

Build on:

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
curl -X POST "http://0.0.0.0:8000/tz-at/" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"lat\":0,\"lng\":0}"
```

The Swagger API documentation can reached at [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs).

## Development

To develop, set up a new clean virtual environment and install the requirements:

```mkvirtualenv
mkvirtualenv --python=/usr/bin/python3.7 tzapi
pip3 install -r requirements.txt
pip3 install -r requirements-dev.txt
```