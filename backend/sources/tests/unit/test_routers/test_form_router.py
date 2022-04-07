import json
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))

import main
import time
import random
import unittest
from main import init_state
import database

from fastapi.testclient import TestClient

class TestFormEndpointNoAuthChecks(unittest.TestCase):
    def setUpClass() -> None:
        init_state()
        # disable authentication checks
        main.routers.AUTHENTICATION_CHECKS = False

    def test_preview_endpoint(self):
        """
        Send a correct message and expect to receive a valid answer.
        """
        client = TestClient(main.app)
        form = {
            "title": "test_form",
            "formId": "some form id",
            "description": "a sample form",
            "questions": [
                {
                    "title": "A question",
                    "description": "a description",
                    "maxAnswerLength": 10,
                },
            ],
            "canBeFilledOnline": True,
            "needsToBeSignedInToSubmit": True,
            "authorEmail": "test@test.com",
        }
        response = client.post("/api/form/preview", json=form)
        self.assertEqual(response.status_code, 200)   
        self.assertTrue("formPdfBase64" in json.loads(response.content))

    def test_create_endpoint(self):
        """
        Send a correct message and expect to receive a valid answer.
        """
        client = TestClient(main.app)
        form = {
            "title": "test_form",
            "formId": "",
            "description": "a sample form",
            "questions": [
                {
                    "title": "A question",
                    "description": "a description",
                    "maxAnswerLength": 10,
                },
            ],
            "canBeFilledOnline": True,
            "needsToBeSignedInToSubmit": True,
            "authorEmail": "test@test.com",
        }
        response = client.post("/api/form/create", json=form)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertTrue("formPdfBase64" in content)
        self.assertTrue("formId" in content)

        nr_in_db = database.get_collection(database.FORMS).count_documents({
            "formId": content["formId"]
        })

        self.assertEqual(nr_in_db, 1)
