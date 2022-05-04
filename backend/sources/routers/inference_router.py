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

@router.post(
    "/infer",
    responses = {
        200: {
            "model": List[Union[smart_forms_types.FormAnswer, str]],
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
    result = pdf_processor.extract_answers_from_files(files)

    # block all unauthorised entries
    for i in range(len(result)):
        if isinstance(result[i], smart_forms_types.FormAnswer) and not can_submit_answer_to_form(result[i].formId):
            result[i] = f"You are not authorized to submit an answer to the form {result[i].formId}"

    # parsed result
    answers = [i for i in result if isinstance(i, smart_forms_types.FormAnswer)]

    # add email to entries
    for answer in answers:
        answer.authorEmail = user_email

    logging.info(f"Performed inference. Found {len(result)} forms, out of which {len(answers)} were valid.")
    # set ids
    for answer in answers:
        answer.answerId = f"entry-{str(random.randint(10**10, 9*10**10))}"
        answer.creationDate = datetime.now()

    # if we have any entries, add them to the DB
    if answers != []:
        db = database.get_collection(database.ENTRIES)
        db.insert_many([answer.to_dict() for answer in answers])

    return result
