from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/api/trips/{trip_id}")
def get_trip(trip_id: str) -> dict:
    return {"trip_id": trip_id, "message": "hello world"}


app.mount("/", StaticFiles(directory="static", html=True), name="static")
