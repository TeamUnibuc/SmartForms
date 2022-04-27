import random
from typing import List
from fastapi import APIRouter, File
from fastapi.responses import PlainTextResponse, Response
from pydantic import BaseModel
import smart_forms_types
import fastapi
import database
import logging

router = APIRouter(
    prefix="/api/entry",
    tags=["entry"]
)

@router.post(
    "/create",
    responses = {
        200: {
            "class": PlainTextResponse,
            "description": "Ok. Returns the entryId"
        },
        400: {
            "description": "Invalid input. Error message."
        }
    }
)
async def submit_entry(entry: smart_forms_types.FormAnswer):
    """
        Submits a new entry for a given form.
        The entry's ID will be overriten, so please use
        /edit to edit an existing entry.
    """
    # TODO: Check permisions and that entry.formID exists.
    db = database.get_collection(database.ENTRIES)
    entry.answerId = f"entry-{str(random.randint(10**10, 9*10**10))}"

    db.insert_one(entry.to_dict())
    return PlainTextResponse(entry.answerId)


@router.delete(
    "/delete/{entryId}",
    responses = {
        200: {
            "description": "Ok."
        },
        400: {
            "description": "Invalid input. Error message."
        }
    }
)
async def delete_entry(entryId: str):
    """
    Deletes an entry with a given ID.
    """
    db = database.get_collection(database.ENTRIES)
    # TODO: Check what is here.
    db.delete_one({ "answerId": entryId })
    return PlainTextResponse("Ok")


@router.post(
    "/edit",
    responses = {
        200: {
            "description": "Ok."
        },
        400: {
            "description": "Invalid input. Error message."
        }
    }
)
async def edit_entry(entry: smart_forms_types.FormAnswer):
    """
    Replaces an entry with the same ID with the new one.
    """
    db = database.get_collection(database.ENTRIES)
    # TODO: Check what is here.
    db.replace_one({ "answerId": entry.answerId }, entry.to_dict())
    return PlainTextResponse("Ok")


@router.get(
    "/view-entry/{entryId}",
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
async def view_entry(entryId: str):
    """
    Returns the entries for a given form.
    """
    db = database.get_collection(database.ENTRIES)
    
    forms = [
        smart_forms_types.form_answer_from_dict(i)
        for i in db.find({ "answerId": entryId })
    ]

    if forms == []:
        return Response(status_code=400, content="Form not found.")
    
    return forms[0]


class ViewEntriesReceiveModel(BaseModel):
    formId: str
    offset: int
    count: int

class ViewEntriesReturnModel(BaseModel):
    entries: List[smart_forms_types.FormAnswer]
    totalFormsCount: int

@router.post(
    "/view-form-entries",
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
    
    entries = [
        smart_forms_types.form_answer_from_dict(i) for i in db.find(
            { "formId": params.formId }, 
            skip=params.offset,
            limit=params.count
        )
    ]
    nr_forms = db.count_documents({})

    return ViewEntriesReturnModel(
        entries=entries,
        totalFormsCount=nr_forms
    )


