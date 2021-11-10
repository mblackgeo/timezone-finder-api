import os

import uvicorn
from fastapi import FastAPI
from mangum import Mangum
from timezonefinder import TimezoneFinder

from tzfinderapi.models import Coordinates, Timezone

tf = TimezoneFinder(in_memory=True)

# Ensure the docs are served at the correct endpoint
stage = os.environ.get("STAGE", None)
root_path = f"/{stage}" if stage else "/"
app = FastAPI(root_path=root_path)

# Add handler for AWS Lambda
handler = Mangum(app=app)


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/health")
def health():
    return "healthy"


@app.post("/tz-at", response_model=Timezone)
def tz_at(query: Coordinates):
    return Timezone(timezone_id=tf.timezone_at(lat=query.lat, lng=query.lng))


@app.post("/tz", response_model=Timezone)
def tz(query: Coordinates):
    return Timezone(timezone_id=tf.timezone_at(lat=query.lat, lng=query.lng))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
