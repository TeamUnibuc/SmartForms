"""
Base class of a PDF form.
"""
from typing import List
import routers.models
import fpdf

class Square:
    width: float
    x: float
    y: float

    def __init__(self, x, y, width):
        self.width = width
        self.x = x
        self.y = y
class PdfForm:
    """
        Internal representation of a pdf form.
    """
    # actual text within the pdf form
    description: routers.models.FormDescription
    # raw data of the pdf render
    pdf_file: fpdf.FPDF
    
    # Answer squares location in pdf.
    # First dimension is for the questions.
    answer_squares_location: List[List[Square]]

    def __init__(self):
        self.description = None
        self.pdf_file = None
        self.answer_squares_location = None

    def extract_raw_pdf_bytes(self):
        return bytes(self.pdf_file.output("new_pdf.pdf", dest='S'), encoding="ISO-8859-1")