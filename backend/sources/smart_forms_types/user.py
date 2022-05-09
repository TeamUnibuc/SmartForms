
import datetime
from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    """
    Class storing information about a given user.
    This is in addition to the OAUTH tokens we receive.
    """
    # date when the user created the account
    account_creation_date: datetime.datetime

    # last sign in date for the user
    last_sign_in_date: datetime.datetime

    # email of the user, acting as a unique identifier
    email: str

    # url of the picture
    picture: Optional[str]

    # full name
    name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
