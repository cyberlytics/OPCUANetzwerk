# Backend

## Requirements 

Step 1: Create virtualenv (optional)
```bash
python -m venv venv

#Windows
./venv/Scripts/activate

#Linux
source ./venv/bin/activate
```

Step 2: Download requirements
```bash
pip install -r requirements.txt
```

## Database
The app requires a **MongoDB** database. There are three ways to create this locally:

1. Download and run MongoDB from the [official Website](*https://www.mongodb.com/) or from prefered package manager.
    
2. Start via Docker 
```bash 
#check that docker is running 
docker ps 

#start the DB
docker run --name mongodb -d -p 27017-27019:27019-27019 mongo:4.4
```

## Start the app 
The app uses the 'uvicorn' server for providing the API. It can be started with
```bash
python -m backend
```

An alternative would be
```bash
uvicorn backend:app [--flags]
```
## Run tests
Run the test with:
```bash
python -m pytest -s
```
This is possible because the `pytest` library is included in the requirements. The `-s` flag at the end is needed for proper testing setup 

NOTE: Tests can also be started with a simple `pytest -s`, but this requires that the current path was added to `PYTHONPATH` before. Otherwise there could be some errors due to `ModuleNotFoundExceptions`

## Test Coverage

If you want to run the tests and check code coverage, use (`PYTHONPATH` needs to be set):
```bash
pytest -s --cov=backend
```

The current test coverage is: 


