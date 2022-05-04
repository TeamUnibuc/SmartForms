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

    def test_create_and_description_endpoint(self):
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
        self.assertIsNotNone(extracted_form.creationDate)

    def test_list_endpoint(self):
        """
        Creates a form, and expects list to return at least one form.
        """
        form = get_generic_form_description()

        response = self.client.post("/api/form/create", json=form.dict())
        self.assertEqual(response.status_code, 200)        
        content = json.loads(response.content)
        self.assertTrue("formId" in content)

        # try to get form from /list
        response = self.client.post(
            f"/api/form/list",
            json={
                "offset": 0,
                "count": 10
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue("forms" in response.json())
        self.assertGreater(len(response.json()["forms"]), 0)

    def test_pdf_endpoint(self):
        """
        Creates a form, and tries to retrieve it.
        """
        form = get_generic_form_description()

        response = self.client.post("/api/form/create", json=form.dict())
        self.assertEqual(response.status_code, 200)        
        content = json.loads(response.content)
        self.assertTrue("formId" in content)
        form_id = content["formId"]

        # try to get form from /list
        response = self.client.get(
            f"/api/form/pdf/{form_id}"
        )

        content = base64.b64decode(
            str(response.content, encoding="utf-8")
        )

        # try to read content as pdf
        pdf = PdfFileReader(io.BytesIO(content))

        # shouldn't be none
        self.assertIsNotNone(pdf)

        # should have one page
        self.assertEqual(pdf.numPages, 1)

        # should contain the title (form_title)
        self.assertNotEqual(
            pdf.getPage(0).extractText().find("form_title"),
            -1
        )

    def test_delete_endpoint(self):
        """
        Creates a form, and tries to delete it.
        """
        form = get_generic_form_description()

        response = self.client.post("/api/form/create", json=form.dict())
        self.assertEqual(response.status_code, 200)        
        content = json.loads(response.content)
        self.assertTrue("formId" in content)
        form_id = content["formId"]

        # try to get form from /list
        response = self.client.delete(
            f"/api/form/delete/{form_id}"
        )
        
        # no errors deleting the form
        self.assertEqual(response.status_code, 200)

        # try to read the form again
        response = self.client.get(
            f"/api/form/description/{form_id}"
        )

        # should get 203
        self.assertEqual(response.status_code, 203)

    def test_visibility_endpoint(self):
        """
        Creates a form, and tries to delete it.
        """
        form = get_generic_form_description()
        form.canBeFilledOnline = False
        form.needsToBeSignedInToSubmit = False

        response = self.client.post("/api/form/create", json=form.dict())
        self.assertEqual(response.status_code, 200)        
        content = json.loads(response.content)
        self.assertTrue("formId" in content)
        form_id = content["formId"]

        # try to get form from /list
        response = self.client.put(
            f"/api/form/online-access/{form_id}",
            json={
                "canBeFilledOnline": True,
                "needsToBeSignedInToSubmit": True
            }
        )
        
        # no errors deleting the form
        self.assertEqual(response.status_code, 200)

        # try to read the form again
        response = self.client.get(
            f"/api/form/description/{form_id}"
        )

        # should get 200
        self.assertEqual(response.status_code, 200)
        
        extracted_form = smart_forms_types.FormDescription(
            **response.json()
        )

        # should be the same, exept the two fields
        self.assertEqual(extracted_form.formId, form_id)
        self.assertTrue(extracted_form.needsToBeSignedInToSubmit)
        self.assertTrue(extracted_form.canBeFilledOnline)

    
if __name__ == '__main__':
    unittest.main()
    
