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

def init_environment():
    """
        Loads .env and initializes logging.
    """
    load_dotenv()
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def main():
    """
        Starts the FastAPI server.
    """
    init_environment()
    
    app = FastAPI()

    # register a session middleware, for storing authentication
    # status and cookies
    app.add_middleware(SessionMiddleware, secret_key=os.getenv("COOKIES_SECRET"))

    app.include_router(routers.form_router.router)
    app.include_router(routers.entry_router.router)
    app.include_router(routers.inference_router.router)
    app.include_router(routers.user_router.router)

    uvicorn.run(
        app,
        host=os.environ['SERVER_HOST'],
        port=int(os.environ['SERVER_PORT'])
    )

if __name__ == "__main__":
    main()
