from typing import List
from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel
import routers.models as models
import fastapi

router = APIRouter(
    prefix="/entry",
    tags=["entry"]
)

@router.get(
    "/{formId}",
    responses = {
        200: {
            "model": models.FormDescription,
            "description": "Ok."
        },
        400: {
            "description": "Invalid input. Error message."
        }
    }
)
async def entry_get_form(formId: str):
    """
        Returns a description of the form, to be able to show 
        a menu where the user can insert data.
    """
    pass


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
async def entry_submit_form(entry: models.FormAnswer, formId: str):
    """
        Submits a new entry for a given form.
    """
    pass


class ViewEntriesReceiveModel(BaseModel):
    offset: int
    count: int

class ViewEntriesReturnModel(BaseModel):
    forms: List[models.FormAnswer]
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
    return { "status": "ok" }

