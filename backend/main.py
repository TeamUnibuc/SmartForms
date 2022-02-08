"""
Entry point of the backend.
Starts a FastAPI server.
"""

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return { "status": "OK" }

if __name__ == "__main__":
    uvicorn.run(app)