import backend

import pytest
import pymongo
from fastapi import FastAPI
from fastapi.testclient import TestClient

client = TestClient(backend.app)
##############################################
#----------------SETUP------------------------
##############################################
def setup_module(module):
    """Clear the test_table and change the used db table of the backend to this test_table
    This is needed, so that tests don't interfere with other data"""
    
    print('Clear Table test_table')
    backend.database.conn['test_table'].sensors.drop()

    print("Setting the DB Table to 'test_table'")
    backend.sensors_routes.db_categories= backend.database.conn['test_table'].sensors


##############################################
#----------------BASIC TESTS------------------
##############################################
def test_db_connection():
    """First step is to check if a database connection could be established"""
    try:
        backend.database.conn.server_info()
    except pymongo.errors.ServerSelectionTimeoutError:
        #if the server_info() method throws a Timeout Exception -> Test Failed
        assert False, f'App started without DB Connection'

def test_base_path():
    """GET('/') should return a simple string"""
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == f"OPC-UA Sensornetz, Version: {backend.config.VERSION}"

##############################################
#----------------TEARDOWN---------------------
##############################################
def teardown_module(module):
    """Remove (test)collection after the tests.
    If the DB connection fails, this method will also fail"""
    backend.database.conn['test_table'].sensors.drop()
