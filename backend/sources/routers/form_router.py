from typing import List
from fastapi import APIRouter, Response
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
import database
import pdf_processor
import smart_forms_types
from starlette.requests import Request
import routers
import os
import random

router = APIRouter(
    prefix="/api/form",
    tags=["form"]
)

class PreviewFormReturnModel(BaseModel):
    formPdfBase64: str

@router.post(
    "/preview",
    responses = {
        200: {
            "model": PreviewFormReturnModel,
            "description": "Base64 encoding of the PDF file."
        },
        201: {
            "model": str,
            "description": "Invalid input. Error message."
        },
        202: {
            "model": str,
            "description": "User is not authenticated."
        }
    }
)
async def get_form_preview(request: Request, form: smart_forms_types.FormDescription):
    """
        Returns a preview of the pdf generated by a form.
        DOES NOT update the database.
        The created form has a watermark to inform the user it's just a preview.
    """
    if routers.AUTHENTICATION_CHECKS and request.session.get('user') is None:
        return PlainTextResponse("User isn't signed in.", status_code=202)

    try:
        form.formId = os.environ["FORM_ID_PREFIX"]
        model = pdf_processor.create_form_from_description(form, True)
        ret = PreviewFormReturnModel(
            formPdfBase64=model.extract_base_64_encoded_pdf()
        )
        return ret
    except Exception as e:
        return PlainTextResponse(repr(e), status_code=201)


class CreateFormReturnModel(BaseModel):
    formId: str
    formPdfBase64: str

@router.post(
    "/create",
    responses = {
        200: {
            "model": CreateFormReturnModel,
            "description": "Ok. Returns the new ID, and the base64 encoding of the PDF."
        },
        201: {
            "model": str,
            "description": "Invalid input. Error message."
        },
        202: {
            "model": str,
            "description": "User is not authenticated."
        }
    }
)
async def create_form(request: Request, form: smart_forms_types.FormDescription):
    """
        Creates a form, and returns its id and a preview.
    """
    # if checks are enabled, add the email to the form.
    if routers.AUTHENTICATION_CHECKS:
        if request.session.get("user") is None:
            return PlainTextResponse("User isn't signed in.", status_code=202)
        else:
            form.authorEmail = request.session.get("user")["email"]
    try:
        # TODO: have a nice error message if the generation fails due to the
        # form being too large.
        # when creating a form, we manually set the formID to be empty, to avoid
        # collisions.
        form.formId = str(random.randint(10**10, 10**11))
        model = pdf_processor.create_form_from_description(form, False)
        database.get_collection(database.FORMS).insert_one(model.to_dict())
        resp = CreateFormReturnModel(
            formId=model.description.formId,
            formPdfBase64=model.extract_base_64_encoded_pdf()
        )
        return resp
    except Exception as e:
        return PlainTextResponse(repr(e), status_code=201)


class ListFormReceiveModel(BaseModel):
    offset: int
    count: int
    # If isOnwer is true, then only shows forms owned by the user.
    # If isOnwer is false, only shows public editable forms, INCLUDING
    # the forms owned by the user.
    isOnwer: bool

class ListFormReturnModel(BaseModel):
    forms: List[smart_forms_types.FormDescription]
    totalFormsCount: int

@router.post(
    "/list",
    responses = {
        200: {
            "model": ListFormReturnModel,
            "description": "Ok."
        },
        202: {
            "model": str,
            "description": "User is not authenticated."
        },
        400: {
            "description": "Invalid input. Error message."
        }
    }
)
async def get_forms_list(request: Request, params: ListFormReceiveModel):
    """
        Returns the list of all available forms.
        If isOnwer is true, then only forms created by the user will be displayed.
    """
    # if authentication is enabled, just return forms made by the authenticated user
    db_search_params = {}
    if routers.AUTHENTICATION_CHECKS:
        if request.session.get("user") is None and params.isOnwer:
            return PlainTextResponse("User isn't signed in.", status_code=202)
        elif params.isOnwer:
            # get forms we own
            db_search_params["authorEmail"] = request.session.get("user")["email"]
        else:
            # only get forms that can be filled online
            db_search_params["canBeFilledOnline"] = True
    
    db = database.get_collection(database.FORMS)

    forms = [
        smart_forms_types.pdf_form_from_dict(i).description
        for i in db.find(
            db_search_params,
            skip=params.offset,
            limit=params.count
        )
    ]
    nr_forms = db.count_documents(db_search_params)

    return ListFormReturnModel(
        forms=forms,
        totalFormsCount=nr_forms
    )


@router.get(
    "/description/{formId}",
    responses = {
        200: {
            "model": smart_forms_types.FormDescription,
            "description": "Ok."
        },
        201: {
            "model": str,
            "description": "User is not signed in or authorised."
        },
        203: {
            "model": str,
            "description": "Form was not found."
        },
        400: {
            "model": str,
            "description": "Invalid input. Error message."
        }
    }
)
async def get_form_description(request: Request, formId: str):
    """
        Returns the description of a given form.
    """
    db = database.get_collection(database.FORMS)
    forms = [smart_forms_types.pdf_form_from_dict(i).description for i in db.find({"formId": formId})]

    if len(forms) == 0:
        return PlainTextResponse("Form wasn't found.", 203)

    if routers.AUTHENTICATION_CHECKS:
        if request.session.get("user") is None and forms[0].needsToBeSignedInToSubmit:
            return PlainTextResponse("User is not authenticated.", 201)
        if not forms[0].canBeFilledOnline and request.session.get("user")["email"] != forms[0].authorEmail:
            return PlainTextResponse("Form can't be filled online.", 201)

    return forms[0]


@router.get(
    "/pdf/{formId}",
    responses = {
        200: {
            "model": str,
            "description": "Base64 encoding of the form pdf."
        },
        201: {
            "model": str,
            "description": "User is not signed in or authorised."
        },
        203: {
            "model": str,
            "description": "Form wasn't found."
        },
        400: {
            "description": "Invalid input. Error message."
        }
    }
)
async def get_form_pdf(request: Request, formId: str):
    """
        Returns the PDF of a given form.
    """
    db = database.get_collection(database.FORMS)
    forms = [smart_forms_types.pdf_form_from_dict(i) for i in db.find({"formId": formId})]

    if len(forms) == 0:
        return PlainTextResponse("Form wasn't found.", 203)

    if routers.AUTHENTICATION_CHECKS:
        if request.session.get("user") is None and forms[0].needsToBeSignedInToSubmit:
            return PlainTextResponse("User is not authenticated.", 201)
        if not forms[0].canBeFilledOnline and request.session.get("user")["email"] != forms[0].authorEmail:
            return PlainTextResponse("Form can't be filled online.", 201)

    return Response(forms[0].extract_base_64_encoded_pdf())


@router.delete(
    "/delete/{formId}",
    responses = {
        200: {
            "description": "Ok."
        },
        201: {
            "model": str,
            "description": "User is not authenticated."
        },
        202: {
            "model": str,
            "description": "User is not owner of the form."
        },
        203: {
            "model": str,
            "description": "Form wasn't found."
        },
        400: {
            "description": "Invalid input. Error message."
        }
    }
)
async def delete_form(request: Request, formId: str):
    """
        Deletes a form. The user has to be the owner.
    """
    db = database.get_collection(database.FORMS)
    forms = [smart_forms_types.pdf_form_from_dict(i) for i in db.find({"formId": formId})]

    if len(forms) == 0:
        return PlainTextResponse("Form wasn't found.", status_code=203)

    if routers.AUTHENTICATION_CHECKS:
        if request.session.get("user") is None:
            return PlainTextResponse("User isn't signed in.", status_code=201)
        elif forms[0].description.authorEmail != request.session.get("user")["email"]:
            return PlainTextResponse("User isn't the owner of the form.", status_code=202)
            
    # delete the form and all of its answers
    db.delete_one({"formId": formId})
    db_entries = database.get_collection(database.ENTRIES)
    db_entries.delete_many({ "formId": formId })
    return { "status": "ok" }


class UpdateFormReceiveModel(BaseModel):
    canBeFilledOnline: bool
    needsToBeSignedInToSubmit: bool

@router.put(
    "/online-access/{formId}",
    responses = {
        200: {
            "description": "Ok."
        },
        201: {
            "model": str,
            "description": "User is not authenticated."
        },
        202: {
            "model": str,
            "description": "User is not owner of the form."
        },
        203: {
            "model": str,
            "description": "Form wasn't found."
        },
        400: {
            "description": "Invalid input. Error message."
        }
    }
)
async def update_form_visibility(request: Request, params: UpdateFormReceiveModel, formId: str):
    """
        Updates online visibility of a form.
        Note: This does not affect the owner of the form.
    """
    db = database.get_collection(database.FORMS)
    forms = [smart_forms_types.pdf_form_from_dict(i) for i in db.find({"formId": formId})]
    
    if len(forms) == 0:
        return PlainTextResponse("Form wasn't found.", status_code=203)

    if routers.AUTHENTICATION_CHECKS:
        if request.session.get("user") is None:
            return PlainTextResponse("User isn't signed in.", status_code=201)
        elif forms[0].description.authorEmail != request.session.get("user")["email"]:
            return PlainTextResponse("User isn't the owner of the form.", status_code=202)
    

    form = forms[0]
    form.description.needsToBeSignedInToSubmit = params.needsToBeSignedInToSubmit
    form.description.canBeFilledOnline = params.canBeFilledOnline

    db.replace_one({ "formId": formId }, form.to_dict())
    return PlainTextResponse("Ok")
