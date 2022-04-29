import logging
import pymongo
import os
import smart_forms_types

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

def get_form_by_id(form_id: str) -> smart_forms_types.PdfForm:
    """
    Returns a form description for a given id.
    Throws an exception if no form is found.
    """
    form_dict = [i for i in get_collection(FORMS).find({ "formId": form_id })]

    # unable to find form
    if len(form_dict) == 0:
        raise Exception(f"Unable to find form {form_id} on mongo cloud!")

    form = smart_forms_types.pdf_form_from_dict(form_dict[0])
    return form

def get_entry_by_id(entry_id: str) -> smart_forms_types.FormAnswer:
    """
    Returns a form description for a given id.
    Throws an exception if no form is found.
    """
    entry_dict = get_collection(ENTRIES).find_one({ "answerId": entry_id })

    # unable to find form
    if entry_dict is None:
        raise Exception(f"Unable to find entry {entry_id} on mongo cloud!")

    entry = smart_forms_types.form_answer_from_dict(entry_dict)
    return entry
