import base64
import json
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))

import main
import time
import random
import unittest
from main import init_state
import database
import smart_forms_types
from PyPDF2 import PdfFileReader
from fastapi.testclient import TestClient
import io


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

class TestUserRouter(unittest.TestCase):
    def setUpClass() -> None:
        init_state()
    
    def setUp(self) -> None:
        self.client = TestClient(main.app)

    def test_details_not_logged_in(self):
        """
        Send a message while not logged in, and expect to be told so.
        """
        response = self.client.get("/api/user/details")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_signed_in" in response.json())
        self.assertFalse(response.json()["is_signed_in"])

    def todo_test_details_signed_in(self):
        """
        TODO: See how to integrate session in unit tests.
        Send a message while logged in, and expect to receive back the info.
        """
        response = self.client.get(
            "/api/user/details", 
            cookies={
                "user": "yep"
                # "user": {
                #     "picture": "picture url",
                #     "email": "email@gmail.com",
                #     "name": "Name",
                #     "given_name": "Given Name",
                #     "family_name": "Family Name"
                # }
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_signed_in" in response.json())
        self.assertTrue(response.json()["is_signed_in"])

        user = response.json()["user"]
        self.assertEqual(user["email"], "email@gmail.com")
        

if __name__ == '__main__':
    unittest.main()

