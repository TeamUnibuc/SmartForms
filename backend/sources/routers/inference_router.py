from typing import List, Union
from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel
from starlette.requests import Request
import smart_forms_types
import pdf_processor

router = APIRouter(
    prefix="/api/inference",
    tags=["inference"]
)

@router.post(
    "/infer",
    responses = {
        200: {
            "model": List[Union[smart_forms_types.FormAnswer, str]],
            "description": "Ok. Each item is an answer, if found," +\
                    "or a string if an error occured for that particular form."
        },
        400: {
            "description": "Invalid input. Error message."
        }
    }
)
async def extract_answer(request: Request, fileUploads: List[UploadFile] = File(...)):
    """
        Extracts data from a form.
        Conditions:
            1. All image files attached must make EXACTLY ONE form.
            2. Each PDF must be EXACLY ONE form.
            3. In each zip, in each folder of the zip (including /), the same rules apply.
    """
    # TODO: Add them to the DB
    files = [
        (file.file.read(), file.filename) for file in fileUploads
    ]

    # TODO:
    # maybe we should add the answers in the DB here
    answer = pdf_processor.extract_answers_from_files(files)
    return answer
