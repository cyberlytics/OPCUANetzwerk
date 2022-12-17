#meta configs
VERSION = '0.1'

#DB connection configs
MONGO_PORT = 27017 #default mongo port
MONGO_HOST = 'localhost' #'mongodb' if run both services are run via docker-compose
MONGO_URI  = f'mongodb://{MONGO_HOST}:{MONGO_PORT}/'
MONGO_URI_DEFAULT = f'mongodb://mongodb:27017/'
DB_NAME = 'sensornetz'

#server configs
HOST = '0.0.0.0'
PORT = 8000
LOG_LEVEL='info'
CORS_ORIGINS = ['*']

#OPC-UA configs
#SENSOR_NETWORK_URL = 'opc.tcp://127.0.0.1:4841' -> Dev server
SENSOR_NETWORK_URL = 'opc.tcp://server.sn.local:4841'

#App settings
COLLECT_TIMEWINDOW_SECONDS = 120 #every xxx seconds, collect all sensor values and store them in the DB