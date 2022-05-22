from datetime import datetime
import logging
import random
from typing import List, Union
from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel
from starlette.requests import Request
import smart_forms_types
import pdf_processor
import database
import routers

router = APIRouter(
    prefix="/api/inference",
    tags=["inference"]
)

class InferenceReturnModel(BaseModel):
    entries: List[smart_forms_types.FormAnswer]
    errors: List[str]

@router.post(
    "/infer",
    responses = {
        200: {
            "model": InferenceReturnModel,
            "description": "Ok. Each item is an answer, if found," +\
                    "or a string if an error occured for that particular answer."
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
    user_email = ""
    if request.session.get("user") is not None:
        user_email = request.session.get("user")["email"]

    def can_submit_answer_to_form(formId):
        """
        returns if we can submit an answer to a given form
        """
        form = database.get_form_by_id(formId)

        # no checks
        if not routers.AUTHENTICATION_CHECKS:
            return True

        # we own the form
        if user_email == form.description.authorEmail:
            return True

        # we can't submit online
        if not form.description.canBeFilledOnline:
            return False

        # we are not authenticated
        if form.description.needsToBeSignedInToSubmit and user_email == "":
            return False

        # otherwise, we can submit it
        return True

    files = [
        (file.file.read(), file.filename) for file in fileUploads
    ]

    # perform inference
    inference_result = pdf_processor.extract_answers_from_files(files)
    errors = []
    entries = []

    # block all unauthorised entries
    for answer, images in inference_result:
        if not can_submit_answer_to_form(answer.formId):
            errors.append(f"You are not authorized to submit an answer to the form {answer.formId}")
        else:
            # set additional properties
            answer.answerId = f"entry-{smart_forms_types.generate_uuid()}"
            answer.creationDate = datetime.now()
            answer.authorEmail = user_email

            # push characters to the database
            smart_forms_types.InferedCharacter.populate_database_from_answer(
                answer,
                images
            )

            # save the entry
            entries.append(answer)

    logging.info(f"Performed inference. Found {len(entries)} answers, and encountered {len(errors)} permission issues.")
    
    # if we have any entries, add them to the DB
    if entries != []:
        db = database.get_collection(database.ENTRIES)
        db.insert_many([answer.dict() for answer in entries])

    return InferenceReturnModel(entries=entries, errors=errors)
