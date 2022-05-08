from datetime import datetime
import random
from typing import List
from fastapi import APIRouter, File, Request
from fastapi.responses import PlainTextResponse, Response
from pydantic import BaseModel
import smart_forms_types
import fastapi
import database
import logging
import routers

router = APIRouter(
    prefix="/api/entry",
    tags=["entry"]
)

@router.post(
    "/create",
    responses = {
        200: {
            "model": str,
            "description": "Ok. Returns the entryId"
        },
        201: {
            "model": str,
            "description": "Form with given ID was not found." 
        },
        202: {
            "model": str,
            "description": "User is not authenticated."
        },
        203: {
            "model": str,
            "description": "User is not authorized."
        },
        400: {
            "description": "Invalid input. Error message."
        }
    }
)
async def submit_entry(request: Request, entry: smart_forms_types.FormAnswer):
    """
        Submits a new entry for a given form.
        The entry's ID will be overriten, so please use
        /edit to edit an existing entry.
        For submiting an entry:
            * Authentication checks must be disabled, or
            * canBeFilledOnline true, and needsToBeSignedInToSubmit true, or
            * CanBeFilledOnline true, and user is signed in, or
            * user is the creator of the form
    """
    user_email = ""
    if request.session.get("user") is not None:
        user_email = request.session.get("user")["email"]

    form_id = entry.formId
    try:
        form = database.get_form_by_id(form_id)
    except:
        return PlainTextResponse(f"Unable to find form {form_id} in our database.", 201)
    
    # set email and time
    entry.authorEmail = user_email
    entry.creationDate = datetime.now()
    
    # user needs to be signed in to submit the form
    if form.description.needsToBeSignedInToSubmit and user_email == "":
        return PlainTextResponse("The user needs to be authenticated to submit to this form.", 202)

    # form can't be filled online
    if not form.description.canBeFilledOnline and user_email != form.description.authorEmail:
        return PlainTextResponse("The user isn't allowed to submit to this form.", 203)

    if len(entry.answers) != len(form.description.questions):
        return PlainTextResponse("Number of answers is not valid.", 400)

    db = database.get_collection(database.ENTRIES)
    entry.answerId = f"entry-{smart_forms_types.generate_uuid()}"

    db.insert_one(entry.dict())
    return PlainTextResponse(entry.answerId)


@router.delete(
    "/delete/{entryId}",
    responses = {
        200: {
            "description": "Ok."
        },
        201: {
            "model": str,
            "description": "Entry with given ID was not found." 
        },
        202: {
            "model": str,
            "description": "User is not authenticated."
        },
        203: {
            "model": str,
            "description": "User is not authorized."
        },
        400: {
            "description": "Invalid input. Error message."
        }
    }
)
async def delete_entry(request: Request, entryId: str):
    """
    Deletes an entry with a given ID.
    For deleting an entry:
        * authentication checks are disabled, or
        * User is the creator of the entry, or
        * User is the creator of the form
    """
    user_email = ""
    if request.session.get("user") is not None:
        user_email = request.session.get("user")["email"]

    try:
        entry = database.get_entry_by_id(entryId)
    except Exception  as e:
        return PlainTextResponse(f"Entry with id {entryId} not found!", 201)

    # we make sure to never have an orphan entry, so this shouldn't have any issues.
    form = database.get_form_by_id(entry.formId)

    # user has to be signed in to delete an entry.
    if routers.AUTHENTICATION_CHECKS and user_email == "":
        return PlainTextResponse("User isn't authenticated.", 202)

    # user has to own the form or the entry to delete it.
    if routers.AUTHENTICATION_CHECKS and user_email != entry.authorEmail and user_email != form.description.authorEmail:
        return PlainTextResponse("User isn't authorized to delete the entry.", 203)

    # delete the entry from the database
    db = database.get_collection(database.ENTRIES)
    db.delete_one({ "answerId": entryId })
    return PlainTextResponse("Ok")


@router.put(
    "/edit",
    responses = {
        200: {
            "description": "Ok."
        },
        201: {
            "model": str,
            "description": "Entry with given ID was not found." 
        },
        202: {
            "model": str,
            "description": "User is not authenticated."
        },
        203: {
            "model": str,
            "description": "User is not authorized."
        },
        400: {
            "description": "Invalid input. Error message."
        }
    }
)
async def edit_entry(request: Request, entry: smart_forms_types.FormAnswer):
    """
    Replaces an entry with the same ID with the new one.
    For editing an entry:
        * authentication checks are disabled, or
        * User is the creator of the entry, or
        * User is the creator of the form
    """

    user_email = ""
    if request.session.get("user") is not None:
        user_email = request.session.get("user")["email"]

    try:
        entry_db = database.get_entry_by_id(entry.answerId)
    except:
        return PlainTextResponse(f"Entry with id {entry.answerId} not found!", 201)

    # we make sure to never have an orphan entry, so this shouldn't have any issues.
    form = database.get_form_by_id(entry_db.formId)

    # entries should 
    # user has to be signed in to delete an entry.
    if routers.AUTHENTICATION_CHECKS and user_email == "":
        return PlainTextResponse("User isn't authenticated.", 202)

    # user has to own the form or the entry to delete it.
    if routers.AUTHENTICATION_CHECKS and user_email != entry_db.authorEmail and user_email != form.description.authorEmail:
        return PlainTextResponse("User isn't authorized to edit the entry.", 203)

    if len(entry.answers) != len(form.description.questions):
        return PlainTextResponse("Number of answers is not valid.", 400)
    
    if entry.formId != form.description.formId:
        return PlainTextResponse("Entry can't change its formId.", 400)

    entry_db.answers = entry.answers
    entry_db.creationDate = datetime.now()

    db = database.get_collection(database.ENTRIES)
    # TODO: Check what is here.
    db.replace_one({ "answerId": entry.answerId }, entry_db.dict())
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
        smart_forms_types.FormAnswer(**i)
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
        203: {
            "model": str,
            "description": "User is not authorized."
        },
        400: {
            "description": "Invalid input. Error message."
        }
    }
)
async def view_entries(request: Request, params: ViewEntriesReceiveModel):
    """
    Returns the entries for a given form.
    """
    user_email = ""
    if request.session.get("user") is not None:
        user_email = request.session.get("user")["email"]

    try:
        form = database.get_form_by_id(params.formId)
    except:
        return PlainTextResponse(f"Form with id {params.formId} not found!", 201)

    if routers.AUTHENTICATION_CHECKS and user_email != form.description.authorEmail:
        return PlainTextResponse("User is not authorized.", 203)
        
    db = database.get_collection(database.ENTRIES)
    
    entries = [
        smart_forms_types.FormAnswer(**i) for i in db.find(
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


