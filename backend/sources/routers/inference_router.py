from typing import List
from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel
import routers.models as models
import fastapi

router = APIRouter(
    prefix="/inference",
    tags=["inference"]
)

@router.post(
    "/",
    responses = {
        200: {
            "model": models.FormAnswer,
            "description": "Ok."
        },
        400: {
            "description": "Invalid input. Error message."
        }
    }
)
async def extract_answer(files: List[UploadFile] = File(...)):
    """
        Extracts data from a form.
    """
    pass
