"""
Base class of a PDF form.
"""
from typing import List
import routers.models

class Square:
    width: float
    x: float
    y: float

class PdfForm:
    """
        Internal representation of a pdf form.
    """
    # actual text within the pdf form
    description: routers.models.FormDescription
    # raw data of the pdf render
    pdf_file: bytes
    
    # Answer squares location in pdf.
    # First dimension is for the questions.
    answer_squares_location: List[List[Square]]

    def __init__(self):
        self.description = None
        self.pdf_file = None
        self.answer_squares_location = None