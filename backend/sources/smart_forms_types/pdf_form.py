"""
Base class of a PDF form.
"""
import pickle
import random
from typing import List

from pydantic import BaseModel
# not importing smart_forms_types to not create
# a circular dependency
import smart_forms_types.models as models
import fpdf
import base64

class Square:
    width: float
    x: float
    y: float
    # page the square is in, indexed from 0
    page: int

    def __init__(self, x, y, width, page):
        self.width = width
        self.x = x
        self.y = y
        self.page = page

    @staticmethod
    def from_dict(d: dict):
        return Square(
            x=d["x"],
            y=d["y"],
            width=d["width"],
            page=d["page"]
        )

    def dict(self):
        return {
            "width": self.width,
            "x": self.x,
            "y": self.y,
            "page": self.page
        }

class PdfForm:
    """
        Internal representation of a pdf form.
    """
    # actual text within the pdf form
    description: models.FormDescription
    # raw data of the pdf render
    pdf_file: fpdf.FPDF
    
    # Answer squares location in pdf.
    # First dimension is for the questions.
    answer_squares_location: List[List[Square]]

    def __init__(self, description, pdf_file, answer_squares_location):
        self.description = description
        self.pdf_file = pdf_file
        self.answer_squares_location = answer_squares_location

    def extract_raw_pdf_bytes(self):
        return bytes(self.pdf_file.output("new_pdf.pdf", dest='S'), encoding="ISO-8859-1")

    def extract_base_64_encoded_pdf(self):
        return base64.b64encode(self.extract_raw_pdf_bytes())

    @staticmethod
    def from_dict(d: dict):
        return PdfForm(
            description=models.FormDescription(**d["description"]),
            pdf_file=pickle.loads(d["pdf_file"]),
            answer_squares_location=[
                [Square.from_dict(i) for i in v]
                for v in d["answer_squares_location"]
            ]
        )

    def dict(self) -> dict:
        return {
            "formId": self.description.formId,
            "authorEmail": self.description.authorEmail,
            "description": self.description.dict(),
            "pdf_file": pickle.dumps(self.pdf_file),
            "answer_squares_location": [
                [i.dict() for i in l]
                for l in self.answer_squares_location
            ]
        }

# def pdf_form_from_dict(d: dict) -> PdfForm:
#     return pickle.loads(d["content"])