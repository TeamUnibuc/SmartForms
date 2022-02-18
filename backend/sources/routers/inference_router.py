from typing import List
from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel
import smart_forms_types

router = APIRouter(
    prefix="/api/inference",
    tags=["inference"]
)

@router.post(
    "/",
    responses = {
        200: {
            "model": smart_forms_types.FormAnswer,
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
