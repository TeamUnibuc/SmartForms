from typing import List
from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel
import smart_forms_types
import fastapi
import database
import logging

router = APIRouter(
    prefix="/api/entry",
    tags=["entry"]
)

@router.get(
    "/{formId}",
    responses = {
        200: {
            "model": smart_forms_types.FormDescription,
            "description": "Ok."
        },
        201: {
            "description": "Form doesn't exist or can't be filled online."
        }
    }
)
async def entry_get_form(formId: str):
    """
        Returns a description of the form, to be able to show 
        a menu where the user can insert data.
    """
    db = database.get_collection(database.FORMS)
    forms = [smart_forms_types.pdf_form_from_dict(i).description for i in db.find({"formId": formId})]

    if len(forms) > 1:
        raise Exception("Found multiple forms with same Id!")
    
    if len(forms) == 0:
        logging.info(f"Form {formId} was requested, but not found on server.")
        raise Exception("No form found!")
    
    form = smart_forms_types.pdf_form_from_dict(forms[0]).description
    if not form.canBeFilledOnline:
        raise Exception("Form has to be filled online")

    return smart_forms_types.pdf_form_from_dict(forms[0]).description


@router.post(
    "/{formId}",
    responses = {
        200: {
            "description": "Ok."
        },
        400: {
            "description": "Invalid input. Error message."
        }
    }
)
async def entry_submit_form(entry: smart_forms_types.FormAnswer, formId: str):
    """
        Submits a new entry for a given form.
    """
    db = database.get_collection(database.ENTRIES)

    db.insert_one(entry.to_dict())
    return "ok"


class ViewEntriesReceiveModel(BaseModel):
    offset: int
    count: int

class ViewEntriesReturnModel(BaseModel):
    forms: List[smart_forms_types.FormAnswer]
    totalFormsCount: int

@router.get(
    "/view/{formId}",
    responses = {
        200: {
            "model": ViewEntriesReturnModel,
            "description": "Ok."
        },
        400: {
            "description": "Invalid input. Error message."
        }
    }
)
async def view_entries(params: ViewEntriesReceiveModel):
    """
        Returns the entries for a given form.
    """
    db = database.get_collection(database.ENTRIES)
    
    forms = [smart_forms_types.form_answer_from_dict(i) for i in db.find(skip=params.offset, limit=params.count)]
    nr_forms = db.count_documents({})

    return ViewEntriesReturnModel(
        forms=forms,
        totalFormsCount=nr_forms
    )


