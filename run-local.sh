#!/usr/bin/env bash
docker run -ti \
    --net=host \
    -e ENV='test' \
    "tzfinderapi:latest" \
    "$@"