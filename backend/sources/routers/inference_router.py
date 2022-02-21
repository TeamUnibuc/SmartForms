from typing import List, Union
from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel
import smart_forms_types
import pdf_processor

router = APIRouter(
    prefix="/api/inference",
    tags=["inference"]
)

@router.post(
    "/",
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
async def extract_answer(files: List[UploadFile] = File(...)):
    """
        Extracts data from a form.
        For now, only accepted types are .pdf and .jpg
    """
    answers = []
    for file in files:
        _, answer = pdf_processor.extract_answer_from_form(file.file.read(), file.filename)
        answers.append(answer)
    return answers
