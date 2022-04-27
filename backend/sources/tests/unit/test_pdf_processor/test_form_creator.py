import json
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))


from main import init_state
import main
import time
import io
import random
import unittest
import pdf_processor
import smart_forms_types
from PyPDF2 import PdfFileReader 
import pdf2image
import numpy as np
import pyzbar.pyzbar as pyzbar

from fastapi.testclient import TestClient

def get_generic_form_description():
    """
    returns a generic description used for testing
    contains 2 questions. First is a text question, second is a multiple choice question
    """
    return smart_forms_types.FormDescription(
        title="form_title",
        formId="formId",
        description="Description",
        questions=[
            smart_forms_types.FormTextQuestion(
                title="question_title",
                description="question description",
                maxAnswerLength=12
            ),
            smart_forms_types.FormMultipleChoiceQuestion(
                title="question2_title",
                description="question 2 description",
                choices = ["Yes", "No", "Maybe"]
            )
        ],
        canBeFilledOnline=True,
        needsToBeSignedInToSubmit=False,
        authorEmail=True
    )

def get_content_from_pdf(pdf: smart_forms_types.PdfForm) -> PdfFileReader:
    """
    Parses the content from a pdf file
    """
    return PdfFileReader(io.BytesIO(pdf.extract_raw_pdf_bytes()))

class TestFormCreator(unittest.TestCase):
    def setUpClass() -> None:
        init_state()
        
    def test_pdf_construction(self):
        """
        Test generating a default pdf document.
        """
        form_description = get_generic_form_description()
        pdf_form = pdf_processor.create_form_from_description(form_description, True)
        self.assertEqual(pdf_form.description, form_description)
        self.assertTrue(len(pdf_form.extract_base_64_encoded_pdf()) > 0)

    def test_pdf_preview_watermark(self):
        """
        Checks the watermark is present iff preview is True
        """
        form_desciption = get_generic_form_description()
        # force multiple pages
        form_desciption.questions[0].maxAnswerLength = 500
        # get description w/ and w/o preview
        pdf_form_preview = pdf_processor.create_form_from_description(form_desciption, True)
        pdf_form_no_preview = pdf_processor.create_form_from_description(form_desciption, False)
        # extract content
        content_preview = get_content_from_pdf(pdf_form_preview)
        content_no_preview = get_content_from_pdf(pdf_form_no_preview)

        # they shoud have the same number of pages
        self.assertEqual(content_preview.numPages, content_no_preview.numPages)

        # They should have at least 2 pages
        self.assertGreaterEqual(content_preview.numPages, 2)

        # one shoud contain preview, the other shouldn't
        for page_nr in range(0, content_preview.numPages):
            text_preview: str = content_preview.getPage(page_nr).extractText()
            text_no_preview: str = content_no_preview.getPage(page_nr).extractText()

            self.assertNotEqual(text_preview.find("PREVIEW"), -1)
            self.assertEqual(text_no_preview.find("PREVIEW"), -1)


    def test_pdf_page_counting(self):
        """
        Checks the page conter is present iff there are at least 2 pages
        """
        form_desciption = get_generic_form_description()
        long_form_description = get_generic_form_description()
        # force multiple pages
        long_form_description.questions[0].maxAnswerLength = 500
        # get forms
        pdf_form = pdf_processor.create_form_from_description(form_desciption, True)
        long_pdf_form = pdf_processor.create_form_from_description(long_form_description, False)
        # extract content
        content = get_content_from_pdf(pdf_form)
        long_content = get_content_from_pdf(long_pdf_form)

        # short one should have one page
        self.assertEqual(content.numPages, 1)

        # long one should have at least 2 pages
        self.assertGreaterEqual(long_content.numPages, 2)

        # first one should contain "Page 1"
        self.assertEqual(
            content.getPage(0).extractText().find("Page 1"),
            -1
        )

        # second one should for each page contain "Page i/j"
        for page_id, page in enumerate(long_content.pages):
            self.assertNotEqual(
                page.extractText().find(f"Page {page_id + 1}/{long_content.numPages}"),
                -1
            )

    def test_square_location_is_saved(self):
        """
        Test generating a pdf document with a few questions.
        """
        form_description = smart_forms_types.FormDescription(
            title="form_title",
            formId="formId",
            description="Description",
            questions=[
                smart_forms_types.FormTextQuestion(
                    title="question_title",
                    description="question description",
                    maxAnswerLength=12
                ),
                smart_forms_types.FormTextQuestion(
                    title="question_title",
                    description="question description",
                    maxAnswerLength=10
                )
            ],
            canBeFilledOnline=True,
            needsToBeSignedInToSubmit=False,
            authorEmail=True
        )

        pdf_form = pdf_processor.create_form_from_description(form_description, False)
        self.assertEqual(pdf_form.description, form_description)
        self.assertTrue(len(pdf_form.extract_base_64_encoded_pdf()) > 0)
        self.assertEqual(len(pdf_form.answer_squares_location), 2)
        self.assertEqual(len(pdf_form.answer_squares_location[0]), 12)
        self.assertEqual(len(pdf_form.answer_squares_location[1]), 10)
        # pages for squares are indexed from 0
        self.assertEqual(pdf_form.answer_squares_location[0][0].page, 0)

    def test_qr_code_is_corectly_generated(self):
        """
        Checks the QR code is valid, and each page gets a different one.
        """
        description = get_generic_form_description()
        description.formId = "MyFormId123"
        description.questions[0].maxAnswerLength = 500 # force multiple pages
        form = pdf_processor.create_form_from_description(
            description,
            False # preview is ignored when computing QR code, so we don't really care
        )

        # extract each page as a numpy image
        pages = pdf2image.convert_from_bytes(form.extract_raw_pdf_bytes())
        pages = [np.array(page) for page in pages]

        for page_nr, page in enumerate(pages):
            qr_codes = pyzbar.decode(page)
            # extactly one QR code should be found, which is our id
            page_id = description.formId
            if page_nr > 0:
                page_id += f"?page={page_nr + 1}"

            self.assertEqual(len(qr_codes), 1)
            self.assertEqual(str(qr_codes[0].data, encoding='utf-8'), page_id)

if __name__ == '__main__':
    unittest.main()