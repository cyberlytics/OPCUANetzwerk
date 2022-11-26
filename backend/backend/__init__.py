from pkgutil import ImpImporter
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import ForwardRef
from pydantic import BaseModel


from backend import config
from backend import database

app = FastAPI()

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

