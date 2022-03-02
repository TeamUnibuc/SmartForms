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
import os
from starlette.middleware.sessions import SessionMiddleware

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

    # register a session middleware, for storing authentication
    # status and cookies
    app.add_middleware(SessionMiddleware, secret_key=os.environ["COOKIES_SECRET"])

    for router in routers.routers:
        app.include_router(router)

def main():
    """
        Starts the FastAPI server.
    """
    init_state()
    
    uvicorn.run(
        app,
        host=os.environ['SERVER_HOST'],
        port=int(os.environ['SERVER_PORT'])
    )

if __name__ == "__main__":
    main()
