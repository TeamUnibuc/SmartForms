from asyncio.log import logger
import datetime
from typing import Optional
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse, Response
from pydantic import BaseModel
from starlette.config import Config
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
import os

import smart_forms_types
import database

# authentication logic
# taken mostly from
# https://slatebit.com/fastapi/google/oauth/2020/08/16/fastapi_google_oauth_part1.html
# https://github.com/authlib/demo-oauth-client/tree/master/fastapi-google-login
# https://docs.authlib.org/en/latest/client/frameworks.html#frameworks-clients

router = APIRouter(
    prefix="/api/user",
    tags=["user"]
)

config = Config("../.env")
oauth = OAuth(config)

# url with the openid configuration
# used by Google Oauth
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

# register the google client for Oauth
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@router.get('/')
async def show_login_button(request: Request):
    """
    Return a simple HTML page for registering the user.
    """
    user = request.session.get('user')
    if user is not None:
        email = user['email']
        html = (
            f'<pre>Email: {email}</pre><br>'
            '<a href="/docs">documentation</a><br>'
            '<a href="/api/user/logout">logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="/api/user/login/">login</a>')


@router.get('/login')
async def login(request: Request, redirect_link: str = "/"):
    """
    Sends a request to google to authenticate the user, and saves
    in the session what URL to redirect the user afterwards.
    """
    # Save in session where should i redirect user on frontend after login
    request.session['redirect_link'] = redirect_link
    
    # Redirect Google OAuth back to our application
    frontend_url = os.getenv("FRONTEND_URL")
    redirect_url = frontend_url + "/api/user/auth"

    return await oauth.google.authorize_redirect(request, redirect_url)

@router.get('/auth')
async def auth(request: Request):
    """
    Receives from google an OAuth token.
    """
    # Perform Google OAuth
    token = await oauth.google.authorize_access_token(request)

    # handle multiple behaviours the token has:
    # sometimes it gives back a dict with the "userinfo" object
    # other times we have to parse it from the id_token
    # most probably due to various versions of the oauth lib.
    if "userinfo" in token:
        user = token['userinfo']
    else:
        user = await oauth.google.parse_id_token(request, token)

    logger.info(f"User logged in: {user['email']}")

    # Save the user
    request.session['user'] = dict(user)

    # get the user from the database, and create it if not existent
    # then update the last sign-in date
    try:
        user_db = database.get_user_by_email(user["email"])
        user_db.last_sign_in_date = datetime.datetime.now()
        database.update_user(user_db, create=False)
    except:
        # user doesn't exist, he just created the account
        user_db = smart_forms_types.User(
            account_creation_date=datetime.datetime.now(),
            last_sign_in_date=datetime.datetime.now(),
            email=user["email"],
            picture=user["picture"],
            name=user["name"],
            given_name=user["given_name"],
            family_name=user["family_name"]
        )
        database.update_user(user_db, create=True)
    
    # redirect to the url specified by the frontend
    redirect_link = request.session['redirect_link']
    return RedirectResponse(url=redirect_link)


@router.get('/logout')
async def logout(request: Request):
    # Remove the user
    request.session.pop('user', None)

    return RedirectResponse(url='/')


class GetUserDetailsReturnModel(BaseModel):
    # if the used is or not signed in
    is_signed_in: bool
    # url of the profile picture
    picture: Optional[str]
    email: Optional[str]
    name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]

@router.get(
    "/details",
    responses = {
        200: {
            "model": GetUserDetailsReturnModel,
            "description": "Ok."
        }
    }
)
async def get_user_details(request: Request):
    """
        Returns details from the user.
        If the user is not signed in, then is_signed_in is false, and no other fields are returned.
    """
    print(request.session)
    user = request.session.get('user')

    # the user is not signed in
    if user is None:
        return GetUserDetailsReturnModel(is_signed_in=False)

    # user is a superset of the return values, so we can just return all of it instead
    return GetUserDetailsReturnModel(
        is_signed_in=True,
        picture=user["picture"],
        email=user["email"],
        name=user["name"],
        given_name=user["given_name"],
        family_name=user["family_name"]
    )


@router.delete('/delete-account')
async def logout(request: Request):
    """
    Deletes the user from the database, together with all of
    its forms.
    """
    if "user" not in request.session:
        return PlainTextResponse("User isn't signed in.", 201)

    # extract user
    user_email = request.session["user"]["email"]

    # Remove the user
    request.session.pop('user', None)

    # delete the user from the database
    database.get_collection(database.USERS).delete_many({ "email": user_email })

    # delete the forms created by the user
    db_forms = database.get_collection(database.FORMS)
    db_entries = database.get_collection(database.ENTRIES)

    user_forms = [
        smart_forms_types.PdfForm.from_dict(i)
        for i in db_forms.find({ "authorEmail": user_email })
    ]

    for form in user_forms:
        # delete all the entries for the form, and
        # then the form itself
        db_entries.delete_many({ "formId": form.description.formId })
        db_forms.delete_one({ "formId": form.description.formId })

    return PlainTextResponse("Ok.")
