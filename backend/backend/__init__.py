from pkgutil import ImpImporter
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import ForwardRef
from pydantic import BaseModel


from backend import config
from backend import database
from backend.opcua_client import opcua_client
from backend.routes import sensor_routes

app = FastAPI()
app.include_router(sensor_routes.router_sensors)

app.add_middleware(
    CORSMiddleware,
    allow_origins = config.CORS_ORIGINS,
    #allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def read_root():
    return f"OPC-UA Sensornetz, Version: {config.VERSION}"

