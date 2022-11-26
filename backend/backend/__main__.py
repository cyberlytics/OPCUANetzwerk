import uvicorn
from backend import config

uvicorn.run('backend:app', host=config.HOST, port=config.PORT, log_level=config.LOG_LEVEL)