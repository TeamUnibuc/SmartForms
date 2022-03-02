from fastapi import APIRouter
from pydantic import BaseModel
import database

router = APIRouter(
    prefix="/api/statistics",
    tags=["statistics"]
)

class SmartFormsGlobalStatisticsReturnModel(BaseModel):
    """
        Used for displaying cool stuff in the UI about the usage
        of the app. 
        More field can be added
    """
    total_number_of_forms: int
    total_number_of_entries: int

@router.get(
    "/global",
    responses = {
        200: {
            "model": SmartFormsGlobalStatisticsReturnModel,
            "description": "Ok. Returns the statistics."
        }
    }
)
async def get_forms_statistics():
    """
        Creates a form, and returns its id and a preview.
    """
    total_number_of_forms = database.get_collection(database.FORMS).count_documents({})
    total_number_of_entries = database.get_collection(database.ENTRIES).count_documents({})
    
    resp = SmartFormsGlobalStatisticsReturnModel(
        total_number_of_forms=total_number_of_forms,
        total_number_of_entries=total_number_of_entries,
    )
    return resp
