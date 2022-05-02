from asyncio.log import logger
from typing import Optional
from fastapi import APIRouter, Response
from pydantic import BaseModel
from starlette.config import Config
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
import os

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

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@router.get('/')
async def home(request: Request):
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
async def login(request: Request):
    # Save in session where should i redirect user on frontend after login
    request.session['redirect_link'] = request.query_params.get("redirect_link", "")
    # Redirect Google OAuth back to our application

    backend_uri = os.getenv("BACKEND_URL")
    redirect_uri = backend_uri + "/user/auth"
    # request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get('/auth')
async def auth(request: Request):
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

    frontend_uri = os.getenv("FRONTEND_URL")
    redirect_link = request.session['redirect_link']

    return RedirectResponse(url=f"{frontend_uri}{redirect_link}")


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
