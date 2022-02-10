"""
Entry point of the backend.
Starts a FastAPI server.
"""

from typing import List
from fastapi import FastAPI, File, UploadFile
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return { "status": "OK" }

@app.post("/")
async def fun(file: List[UploadFile] = File(...)):
    print(file[0].filename)
    # f = File(file[0])
    # with open("file.pdf", "wb") as fout:
    #     fout.write(file[0])
    # print(f)
    # print(file)
    return { "status": "OK" }


if __name__ == "__main__":
    uvicorn.run(app)