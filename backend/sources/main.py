"""
Entry point of the backend.
Starts a FastAPI server.
"""

from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
import routers
import logging
import sys
import argparse
import os
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from starlette.middleware.sessions import SessionMiddleware
import ocr.train_network as train_network

# FastAPI app serving the API.
app: FastAPI = None

def init_state():
    """
        Loads .env, initializes logging and creates the webserver.
    """
    global app

    load_dotenv()
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    app = FastAPI(
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )

    # register a session middleware, for storing authentication
    # status and cookies
    app.add_middleware(SessionMiddleware, secret_key=os.environ["COOKIES_SECRET"])

    for router in routers.routers:
        app.include_router(router)

    # register a message on the root
    @app.get('/')
    async def home(request: Request):
        user = request.session.get('user')
        email = user['email'] if user is not None else 'Not signed in'
        
        html = (
                f"<pre>Email: {email}</pre><br>" +
                "<a href='/api/docs'>documentation</a><br>" +
                ("<a href='/api/user/logout'>logout</a>"
                if user is not None else
                "<a href='/api/user/login/'>login</a>")
            )
        return HTMLResponse(html)


def main():
    """
        Starts the FastAPI server, and trains if required.
    """

    parser = argparse.ArgumentParser("smart-forms")
    parser.add_argument("--train", type=str, help="True / False", default='False', required=False)
    args = parser.parse_args()
    train = (args.train in ["True", "true"])

    init_state()

    if train:
        train_network.train_model()
        return

    uvicorn.run(
        app,
        host=os.environ['SERVER_HOST'],
        port=int(os.environ['SERVER_PORT'])
    )

if __name__ == "__main__":
    main()
