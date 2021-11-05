import uvicorn
from fastapi import FastAPI
from timezonefinder import TimezoneFinder

from tzfinderapi.models import Coordinates, Timezone

app = FastAPI()
tf = TimezoneFinder(in_memory=True)


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
