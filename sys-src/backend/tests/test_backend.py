import backend
from tests.test_data import test_data

import pytest
import pymongo
import datetime
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

    print("Insert Test data into db")
    backend.database.conn['test_table'].sensors.insert_many(test_data)

    print("Setting the DB Table for the backend to 'test_table'")
    backend.sensor_routes.db_sensors = backend.database.conn['test_table'].sensors

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
#-------------Test Get Routes-----------------
##############################################
def test_sensor_names():
    """GET('/sensornames') should get all sensor names"""
    response = client.get('/sensornames')
    assert response.status_code == 200


def test_current_values():
    """GET('/sensorvalues/current')should not fail, even if no connection to a OPCUA Server is established"""
    response = client.get('/sensorvalues/current')
    assert response.status_code == 200

def test_timestamp_filter():
    """GET('/sensorvalues') with timestamps"""
    start_time = "2022-01-01T10:10:30.000000"
    end_time = "2022-01-01T10:11:30.000000"
    response = client.get(f'/sensorvalues?startTimestamp={start_time}&endTimestamp={end_time}')
    assert response.status_code == 200
    #only one datapoint matches the time
    assert len(response.json())==1 

    late_start_time = "2022-01-01T10:10:30.000000"
    response = client.get(f'/sensorvalues?startTimestamp={late_start_time}')
    assert response.status_code == 200
    #filter matches all except 2
    assert len(response.json())==2

    early_end_time = "2022-01-01T10:10:30.000000"
    response = client.get(f'/sensorvalues?endTimestamp={early_end_time}')
    assert response.status_code == 200
    #filter should exclude two
    assert len(response.json())==len(test_data)-2


def test_string_filter():
    """GET('/sensorvalues') with different filters"""
    response = client.get('/sensorvalues')
    assert response.status_code == 200

    #test sensornode
    sensornode_param='SensorNode_1'
    test_result = [data_point for data_point in test_data if data_point['sensornode']==sensornode_param]
    response = client.get(f'/sensorvalues?sensornode={sensornode_param}')
    assert response.status_code == 200
    assert len(response.json())== len(test_result)

    #test sensorname
    sensorname_param ='ABC123'
    test_result = [data_point for data_point in test_data if data_point['sensorname']==sensorname_param]
    response = client.get(f'/sensorvalues?sensorname={sensorname_param}')
    assert response.status_code == 200
    assert len(response.json())== len(test_result)
    
    #test sensortyp
    sensortyp_param = 'AirPressure'
    test_result = [data_point for data_point in test_data if data_point['sensortyp']==sensortyp_param]
    response = client.get(f'/sensorvalues?sensortyp={sensortyp_param}')
    assert response.status_code == 200
    assert len(response.json())== len(test_result)

    #combine params
    test_result = [data_point for data_point in test_data if data_point['sensornode']==sensornode_param]
    test_result = [data_point for data_point in test_result if data_point['sensorname']==sensorname_param]
    test_result = [data_point for data_point in test_result if data_point['sensortyp']==sensortyp_param]
    response = client.get(f'/sensorvalues?sensornode={sensornode_param}&sensorname={sensorname_param}&sensortyp={sensortyp_param}')
    assert response.status_code == 200
    assert len(response.json())== len(test_result)

def test_combined_filters():
    """GET('/sensorvalues') with combined filters"""
    uri = "/sensorvalues?sensornode=SensorNode_1&sensorname=ABC123&sensortyp=AirPressure&startTimestamp=2022-01-01T10:10:30.000000&endTimestamp=2022-01-01T10:11:30.000000"
    response = client.get(uri)
    assert response.status_code == 200
    assert len(response.json()) == 1



##############################################
#----------------TEARDOWN---------------------
##############################################
def teardown_module(module):
    """Remove (test)collection after the tests.
    If the DB connection fails, this method will also fail"""
    backend.database.conn['test_table'].sensors.drop()
