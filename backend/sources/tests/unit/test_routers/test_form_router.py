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

class TestFormEndpointNoAuthChecks(unittest.TestCase):
    def setUpClass() -> None:
        init_state()
        # disable authentication checks
        main.routers.AUTHENTICATION_CHECKS = False

    def setUp(self) -> None:
        self.client = TestClient(main.app)

    def test_preview_endpoint(self):
        """
        Send a correct message and expect to receive a valid answer.
        """
        form = get_generic_form_description()
        response = self.client.post("/api/form/preview", json=form.dict())
        self.assertEqual(response.status_code, 200)   
        self.assertTrue("formPdfBase64" in json.loads(response.content))

    def test_create_endpoint(self):
        """
        Send a correct message and expect to receive a valid answer.
        """
        form = get_generic_form_description()

        response = self.client.post("/api/form/create", json=form.dict())
        self.assertEqual(response.status_code, 200)        
        content = json.loads(response.content)
        self.assertTrue("formPdfBase64" in content)
        self.assertTrue("formId" in content)
        form_id = content["formId"]

        # try to get form from /description
        response_description = self.client.get(
            f"/api/form/description/{form_id}"
        )

        self.assertEqual(response_description.status_code, 200)
        extracted_form = smart_forms_types.FormDescription(
            **response_description.json()
        )

        self.assertEqual(extracted_form.formId, form_id)

if __name__ == '__main__':
    unittest.main()
    
