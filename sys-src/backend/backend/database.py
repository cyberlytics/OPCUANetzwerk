import pymongo

from backend import config


def establish_connection(mongo_uri:str) -> pymongo.mongo_client.MongoClient:
    """Try to connect to a MongoDB database using the given mongo_uri.
    If no connection could be made, it tries to establish a connection with the default mongo_uri

    Args:
        mongo_uri (str): string pointing to db in format 'mongodb://{HOST}:{PORT}/'

    Returns:
        pymongo.mongo_client.MongoClient: _description_
    """
    try:
        conn = pymongo.MongoClient(mongo_uri)
        #check if a database connection can be established, otherwise throw Exception
        conn.server_info()
        #if conn is valid, return the Client
        return conn
    except pymongo.errors.ServerSelectionTimeoutError:
        print(f"No database found at mongo_uri: {config.MONGO_URI}")
        
        if mongo_uri != config.MONGO_URI_DEFAULT:
            print('Trying to use default mongo_uri')
            return establish_connection(config.MONGO_URI_DEFAULT)
        
        else:
            return None


conn = establish_connection(config.MONGO_URI)
#conn is only none, when no db was found under the configure mongo_uri or the default mongo_uri
if conn is None:
    print('App has no connected DB')
    print('Server is shutting down')
    exit()
