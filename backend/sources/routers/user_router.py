from asyncio.log import logger
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
    return HTMLResponse('<a href="/api/user/login">login</a>')


@router.get('/login')
async def login(request: Request):
    # Redirect Google OAuth back to our application
    
    redirect_uri = os.getenv("LOGIN_REDIRECT_URL")
    # request.url_for('auth')

    # print(f"redirect URL: {redirect_uri}")

    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.route('/auth')
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

    return RedirectResponse(url='/api/user')


@router.get('/logout')
async def logout(request: Request):
    # Remove the user
    request.session.pop('user', None)

    return RedirectResponse(url='/api/user')




class GetUserDetailsReturnModel(BaseModel):
    # url of the profile picture
    picture: str
    email: str
    name: str
    given_name: str
    family_name: str

@router.get(
    "/details",
    responses = {
        200: {
            "model": GetUserDetailsReturnModel,
            "description": "Ok."
        },
        400: {
            "description": "Not signed in."
        }
    }
)
async def get_user_details(request: Request):
    """
        Returns details from the user.
        If the user is not signed in, then the status 400 is returned instead.
    """
    user = request.session.get('user')
    
    # the user is not signed in
    if user is None:
        return Response(status_code=400)
    
    # user is a superset of the return values, so we can just return all of it instead
    return user
