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
from fastapi.responses import RedirectResponse
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

    app = FastAPI()

    # disable (some of) tensorflow messages
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    # register a session middleware, for storing authentication
    # status and cookies
    app.add_middleware(SessionMiddleware, secret_key=os.environ["COOKIES_SECRET"])

    for router in routers.routers:
        app.include_router(router)

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

    # add a redirect for now, to ease the workflow
    @app.get('/')
    async def redirect_to_user():
        return RedirectResponse("/api/user")
    uvicorn.run(
        app,
        host=os.environ['SERVER_HOST'],
        port=int(os.environ['SERVER_PORT'])
    )

if __name__ == "__main__":
    main()
