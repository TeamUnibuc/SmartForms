from datetime import datetime
from typing import List
from fastapi import APIRouter, Response
from fastapi.responses import PlainTextResponse, JSONResponse
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
            "model": smart_forms_types.FormAnswer,
            "description": "Invalid input. Error message."
        },
        202: {
            "model": smart_forms_types.FormAnswer,
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
    user_email = ""
    if request.session.get("user") is not None:
        user_email = request.session.get("user")["email"]

    if routers.AUTHENTICATION_CHECKS and user_email == "":
        return JSONResponse(
            routers.StatusReturnModel(
                statusCode = 202,
                message = "User is not authenticated!",
            ).dict(),
            202
        )

    try:
        form.formId = os.environ["FORM_ID_PREFIX"]
        model = pdf_processor.create_form_from_description(form, True)
        ret = PreviewFormReturnModel(
            formPdfBase64=model.extract_base_64_encoded_pdf()
        )
        return ret
    except Exception as e:
        return JSONResponse(
            routers.StatusReturnModel(
                statusCode = 201,
                message = repr(e),
            ).dict(),
            201
        )

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
            "model": smart_forms_types.FormAnswer,
            "description": "Invalid input. Error message."
        },
        202: {
            "model": smart_forms_types.FormAnswer,
            "description": "User is not authenticated."
        }
    }
)
async def create_form(request: Request, form: smart_forms_types.FormDescription):
    """
        Creates a form, and returns its id and a preview.
    """
    user_email = ""
    if request.session.get("user") is not None:
        user_email = request.session.get("user")["email"]

    if routers.AUTHENTICATION_CHECKS and user_email == "":
        return JSONResponse(
            routers.StatusReturnModel(
                statusCode = 202,
                message = "User is not authenticated!",
            ).dict(),
            202
        )

    try:
        form.formId = smart_forms_types.generate_uuid()
        form.creationDate = datetime.now()
        form.authorEmail = user_email

        model = pdf_processor.create_form_from_description(form, False)
        database.get_collection(database.FORMS).insert_one(model.dict())
        resp = CreateFormReturnModel(
            formId=model.description.formId,
            formPdfBase64=model.extract_base_64_encoded_pdf()
        )
        return resp
    except Exception as e:
        return JSONResponse(
            routers.StatusReturnModel(
                statusCode = 201,
                message = repr(e),
            ).dict(),
            201
        )


class ListFormReceiveModel(BaseModel):
    offset: int
    count: int
    # If isOwner is true, then only shows forms owned by the user.
    # If isOwner is false, only shows public editable forms, INCLUDING
    # the forms owned by the user.
    isOwner: bool

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
            "model": smart_forms_types.FormAnswer,
            "description": "User is not authenticated."
        }
    }
)
async def get_forms_list(request: Request, params: ListFormReceiveModel):
    """
        Returns the list of all available forms.
        If isOwner is true, then only forms created by the user will be displayed.
    """
    user_email = ""
    if request.session.get("user") is not None:
        user_email = request.session.get("user")["email"]

    # if authentication is enabled, just return forms made by the authenticated user
    db_search_params = {}
    if routers.AUTHENTICATION_CHECKS:
        if user_email == "" and params.isOwner:
            return JSONResponse(
                routers.StatusReturnModel(
                    statusCode = 202,
                    message = "User is not authenticated!",
                ).dict(),
                202
            )
        elif params.isOwner:
            # get forms we own
            db_search_params["authorEmail"] = request.session.get("user")["email"]
        else:
            # only get forms that can be filled online
            db_search_params["canBeFilledOnline"] = True

    db = database.get_collection(database.FORMS)

    forms = [
        smart_forms_types.PdfForm.from_dict(i).description
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
            "model": routers.StatusReturnModel,
            "description": "Form ID was not found."
        },
        202: {
            "model": routers.StatusReturnModel,
            "description": "User is not authenticated."
        },
        203: {
            "model": routers.StatusReturnModel,
            "description": "User is not authorized."
        },
        400: {
            "model": routers.StatusReturnModel,
            "description": "Invalid input. Error message."
        }
    }
)
async def get_form_description(request: Request, formId: str):
    """
        Returns the description of a given form.
    """
    user_email = ""
    if request.session.get("user") is not None:
        user_email = request.session.get("user")["email"]

    try:
        form = database.get_form_by_id(formId)
    except:
        return JSONResponse(
            routers.StatusReturnModel(
                statusCode = 201,
                message = f"Form with id {formId} not found!",
            ).dict(),
            201
        )

    if routers.AUTHENTICATION_CHECKS:
        if user_email == "" and form.description.needsToBeSignedInToSubmit:
            return JSONResponse(
            routers.StatusReturnModel(
                statusCode = 202,
                message = "User is not authenticated!",
            ).dict(),
            202
        )
        if not form.description.canBeFilledOnline and request.session.get("user")["email"] != form.description.authorEmail:
            return JSONResponse(
            routers.StatusReturnModel(
                statusCode = 203,
                message = "User is not authorized to get the description!",
            ).dict(),
            203
        )

    return form.description


class PdfFormReturnModel(BaseModel):
    formPdfBase64: str

@router.get(
    "/pdf/{formId}",
    responses = {
        200: {
            "model": PdfFormReturnModel,
            "description": "Base64 encoding of the form pdf."
        },
        201: {
            "model": routers.StatusReturnModel,
            "description": "Form ID was not found."
        },
        202: {
            "model": routers.StatusReturnModel,
            "description": "User is not authenticated."
        },
        203: {
            "model": routers.StatusReturnModel,
            "description": "User is not authorized."
        },
        400: {
            "model": routers.StatusReturnModel,
            "description": "Invalid input. Error message."
        }
    }
)
async def get_form_pdf(request: Request, formId: str):
    """
        Returns the PDF of a given form.
    """
    user_email = ""
    if request.session.get("user") is not None:
        user_email = request.session.get("user")["email"]

    try:
        form = database.get_form_by_id(formId)
    except:
        return JSONResponse(
            routers.StatusReturnModel(
                statusCode = 201,
                message = f"Form with id {formId} not found!",
            ).dict(),
            201
        )
        
    if routers.AUTHENTICATION_CHECKS:
        if user_email == "" and form.description.needsToBeSignedInToSubmit:
            return JSONResponse(
                routers.StatusReturnModel(
                    statusCode = 202,
                    message = "User is not authenticated!",
                ).dict(),
                202
            )
        if not form.description.canBeFilledOnline and user_email != form.description.authorEmail:
            return JSONResponse(
                routers.StatusReturnModel(
                    statusCode = 203,
                    message = "User is not authorized to view the form!",
                ).dict(),
                203
            )

    return PdfFormReturnModel(
        formPdfBase64=form.extract_base_64_encoded_pdf()
    )


@router.delete(
    "/delete/{formId}",
    responses = {
        200: {
            "description": "Ok."
        },
        201: {
            "model": routers.StatusReturnModel,
            "description": "Form ID was not found."
        },
        202: {
            "model": routers.StatusReturnModel,
            "description": "User is not authenticated."
        },
        203: {
            "model": routers.StatusReturnModel,
            "description": "User is not authorized."
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
    user_email = ""
    if request.session.get("user") is not None:
        user_email = request.session.get("user")["email"]

    try:
        form = database.get_form_by_id(formId)
    except:
        return JSONResponse(
            routers.StatusReturnModel(
                statusCode = 201,
                message = f"Form with id {formId} not found!",
            ).dict(),
            201
        )

    if routers.AUTHENTICATION_CHECKS:
        if user_email == "":
            return JSONResponse(
                routers.StatusReturnModel(
                    statusCode = 202,
                    message = "User is not authenticated!",
                ).dict(),
                202
            )
        if user_email != form.description.authorEmail:
            return JSONResponse(
                routers.StatusReturnModel(
                    statusCode = 203,
                    message = "User is not authorized to delete the form!",
                ).dict(),
                203
            )

    db = database.get_collection(database.FORMS)
    # delete the form and all of its answers
    db.delete_one({"formId": formId})
    db_entries = database.get_collection(database.ENTRIES)
    db_entries.delete_many({ "formId": formId })

    return JSONResponse(
        routers.StatusReturnModel(
            statusCode = 200,
            message = "Ok",
        ).dict(),
        200
    )


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
            "model": routers.StatusReturnModel,
            "description": "Form ID was not found."
        },
        202: {
            "model": routers.StatusReturnModel,
            "description": "User is not authenticated."
        },
        203: {
            "model": routers.StatusReturnModel,
            "description": "User is not authorized."
        },
        400: {
            "model": routers.StatusReturnModel,
            "description": "Invalid input. Error message."
        }
    }
)
async def update_form_visibility(request: Request, params: UpdateFormReceiveModel, formId: str):
    """
        Updates online visibility of a form.
        Note: This does not affect the owner of the form.
    """

    user_email = ""
    if request.session.get("user") is not None:
        user_email = request.session.get("user")["email"]

    try:
        form = database.get_form_by_id(formId)
    except:
        return JSONResponse(
            routers.StatusReturnModel(
                statusCode = 201,
                message = f"Form with id {formId} not found!",
            ).dict(),
            201
        )

    if routers.AUTHENTICATION_CHECKS:
        if user_email == "":
            return JSONResponse(
                routers.StatusReturnModel(
                    statusCode = 202,
                    message = "User is not authenticated!",
                ).dict(),
                202
            )
        if user_email != form.description.authorEmail:
            return JSONResponse(
                routers.StatusReturnModel(
                    statusCode = 203,
                    message = "User is not authorized to delete the form!",
                ).dict(),
                203
            )

    form.description.needsToBeSignedInToSubmit = params.needsToBeSignedInToSubmit
    form.description.canBeFilledOnline = params.canBeFilledOnline

    db = database.get_collection(database.FORMS)
    db.replace_one({ "formId": formId }, form.dict())
    
    return JSONResponse(
        routers.StatusReturnModel(
            statusCode = 200,
            message = "Ok",
        ).dict(),
        200
    )