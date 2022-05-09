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
USERS = "Users"

def get_collection(collection: str):
    return get_database().database.get_collection(collection)

def get_form_by_id(form_id: str) -> smart_forms_types.PdfForm:
    """
    Returns a form description for a given id.
    Throws an exception if no form is found.
    """
    form_dict = get_collection(FORMS).find_one({ "formId": form_id })

    # unable to find form
    if form_dict is None:
        raise Exception(f"Unable to find form {form_id} on mongo cloud!")

    form = smart_forms_types.PdfForm.from_dict(form_dict)
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

    entry = smart_forms_types.FormAnswer(**entry_dict)
    return entry

def get_user_by_email(email: str) -> smart_forms_types.User:
    """
    Returns the user saved in the database for a given email.
    Throws an exception if no user is found.
    """
    user_dict = get_collection(USERS).find_one({ email: email })

    # unable to find user
    if user_dict is None:
        raise Exception(f"Unable to find {email} in the DB")

    user = smart_forms_types.User(**user_dict)
    return user

def update_user(user: smart_forms_types.User, create=True):
    """
    Updates the user, and creates it if it doesn't exist
    """
    if create:
        get_collection(USERS).insert_one(user.dict())
    else:
        get_collection(USERS).replace_one({ "email": user.email }, user.dict())
