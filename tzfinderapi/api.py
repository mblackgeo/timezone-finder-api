import uvicorn
from fastapi import FastAPI
from timezonefinder import TimezoneFinderL

from tzfinderapi.models import Coordinates, Timezone

app = FastAPI()
tf = TimezoneFinderL(in_memory=True)


@app.get("/health")
def health():
    return "healthy"


@app.post("/tz-at/", response_model=Timezone)
def tz_at(query: Coordinates):
    return Timezone(timezone_id=tf.timezone_at(lat=query.lat, lng=query.lng))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
