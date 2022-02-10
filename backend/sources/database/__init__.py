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
            f"{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWORD')}" +
            f"@{os.getenv('MONGO_CLUSTER')}"
        )

        self.database = self.client.get_database(os.getenv("MONGO_DB_NAME"))
        logging.info("Connected to mongo cloud.")
        
    
def get_database() -> Database:
    """
        Returns a Database object.
    """
    if Database.__instance__ is None:
        Database()
    return Database.__instance__