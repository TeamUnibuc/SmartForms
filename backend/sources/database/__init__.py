import logging
import pymongo
import os

class Database:
    __instance__ = None

    def __init__(self):
        if Database.__instance__ is not None:
            raise Exception("Instanciated twice the database!")
        Database.__instance__ = self

        self.client = pymongo.MongoClient(
            f"mongodb+srv://" +
            f"{os.environ['MONGO_USER']}:{os.environ['MONGO_PASSWORD']}" +
            f"@{os.environ['MONGO_CLUSTER']}"
        )

        self.database = self.client.get_database(os.environ["MONGO_DB_NAME"])
        logging.info("Connected to mongo cloud.")
        
    
def get_database() -> Database:
    """
        Returns a Database object.
    """
    if Database.__instance__ is None:
        Database()
    return Database.__instance__

FORMS = "Forms"
ENTRIES = "Entries"

def get_collection(collection: str):
    return get_database().database.get_collection(collection)
