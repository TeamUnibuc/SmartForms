import json
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))


from main import init_state
import main
import time
import random
import unittest
import pdf_processor
import smart_forms_types

from fastapi.testclient import TestClient

class TestFormCreator(unittest.TestCase):
    def setUpClass() -> None:
        init_state()
        
    def test_empty_pdf(self):
        """
        Test generating an empty pdf document.
        """

        form_description = smart_forms_types.FormDescription(
            title="form_title",
            formId="formId",
            description="Description",
            questions=[],
            canBeFilledOnline=True,
            needsToBeSignedInToSubmit=False,
            authorEmail=True
        )

        pdf_form = pdf_processor.create_form_from_description(form_description, True)
        self.assertEqual(pdf_form.description, form_description)
        self.assertTrue(len(pdf_form.extract_base_64_encoded_pdf()) > 0)

    def test_questions_pdf(self):
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
