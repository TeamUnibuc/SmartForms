"""
Entry point of the backend.
Starts a FastAPI server.
"""

from typing import List
from fastapi import FastAPI, File, UploadFile
import uvicorn
import routers

app = FastAPI()

app.include_router(routers.form_router.router)
app.include_router(routers.entry_router.router)
app.include_router(routers.inference_router.router)

# @app.post("/")
# async def fun(file: List[UploadFile] = File(...)):
#     print(file[0].filename)
#     # f = File(file[0])
#     # with open("file.pdf", "wb") as fout:
#     #     fout.write(file[0])
#     # print(f)
#     # print(file)
#     return { "status": "OK" }


if __name__ == "__main__":
    uvicorn.run(app)