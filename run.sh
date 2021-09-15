#!/bin/bash

/usr/local/bin/uvicorn tzfinderapi.api:app \
  --no-access-log \
  --host 0.0.0.0 \
  --port 8000