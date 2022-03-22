from asyncio.log import logger
from fastapi import APIRouter
from starlette.config import Config
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError

# authentication logic
# taken mostly from
# https://slatebit.com/fastapi/google/oauth/2020/08/16/fastapi_google_oauth_part1.html
# https://github.com/authlib/demo-oauth-client/tree/master/fastapi-google-login
# https://docs.authlib.org/en/latest/client/frameworks.html#frameworks-clients

router = APIRouter(
    prefix="/api/user",
    tags=["login"]
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
    redirect_uri = request.url_for('auth')

    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.route('/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    user = token.get('userinfo')
    if user:
        user = dict(user)
    else:
        user = await oauth.google.parse_id_token(request, token)
        user = dict(user)

    request.session['user'] = user
    return RedirectResponse(url='/api/user')

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
