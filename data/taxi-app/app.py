import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.routes import router

logging.basicConfig(format="%(message)s", level=logging.INFO)

app = FastAPI()
app.include_router(router)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
