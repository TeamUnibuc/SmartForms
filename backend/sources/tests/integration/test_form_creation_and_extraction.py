import base64
import io
import json
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

import main
import time
import random
import unittest
import smart_forms_types
from main import init_state
import pdf2image
import numpy as np
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
                maxAnswerLength=500
            ),
            smart_forms_types.FormMultipleChoiceQuestion(
                title="question2_title",
                description="question 2 description",
                choices = ["Yes", "No", "Maybe"]
            )
        ],
        canBeFilledOnline=True,
        needsToBeSignedInToSubmit=False,
    )

class TestBlankFormCreationAndExtraction(unittest.TestCase):
    def setUpClass() -> None:
        init_state()
        main.routers.AUTHENTICATION_CHECKS = False

    def test_create_form_and_infer_it(self):
        # instantiate a client
        client = TestClient(main.app)
        description = get_generic_form_description()
        response = client.post(
            "/api/form/create",
            json=description.dict()
        )
        self.assertEqual(response.status_code, 200)
        form_id = response.json()["formId"]
        form_content_base64 = response.json()["formPdfBase64"]

        # formId should be able to be used in urls
        self.assertTrue(form_id.find('/') == -1 and form_id.find("#") == -1)

        # get each frame of the form
        form_content_binary = base64.b64decode(form_content_base64)
        pages = pdf2image.convert_from_bytes(form_content_binary)
        
        # convert each page to jpg
        pages_jpg = []
        for page_nr, page in enumerate(pages):
            output = io.BytesIO()
            page.save(output, format="JPEG")
            content = output.getvalue()
            pages_jpg.append(("fileUploads", (f"page-{page_nr}.jpg", content, "image/jpeg")))


        # should have at least 2 pages
        self.assertGreaterEqual(len(pages), 2)

        # send the pages to inference
        response = client.post(
            "/api/inference/infer",
            files=pages_jpg
        )

        # we should get an answer, full of spaces
        self.assertEqual(response.status_code, 200)
        results = response.json()

        self.assertEqual(len(results), 1)
        result = results[0]

        self.assertEqual(result["formId"], form_id)
        self.assertTrue(result["answerId"] is not None)
        # TODO: Add an answerId and add to database
        # self.assertTrue(result["answerId"] != "")

        answers = result["answers"]
        self.assertEqual(len(answers), 2)
        self.assertEqual(len(answers[0]), 500)
        self.assertEqual(len(answers[1]), 3)


if __name__ == '__main__':
    unittest.main()
    