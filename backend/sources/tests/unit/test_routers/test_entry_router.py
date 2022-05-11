import json
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))

import main
import time
import random
import unittest
import smart_forms_types
from main import init_state

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
    )

def get_generic_answer():
    """
    returns a generic smart_forms_types.FormAnswer object
    """
    return smart_forms_types.FormAnswer(
        formId="form_id",
        answers=["012345678912", "XXX"]
    )

class TestEntryRouterNotAuthenticated(unittest.TestCase):
    formId: str

    def setUpClass() -> None:
        init_state()
        main.routers.AUTHENTICATION_CHECKS = False
        # create a form we can add entries to
        # we pick a new id each time to not have
        # redefinition conflicts
        client = TestClient(main.app)
        description = get_generic_form_description()

        response = client.post(
            "/api/form/create", 
            json=description.dict()
        )

        TestEntryRouterNotAuthenticated.formId = response.json()["formId"]

        if response.status_code != 200:
            print(f"Unable to create form, received {response.status_code}.")
            print(f"Message: {response.content}")
            print("Tests will fail.")
    
    def setUp(self):
        # instantiate a client
        self.client = TestClient(main.app)

    def test_submit_new_entry(self):
        """
        Try to submit a valid new entry, and check we get back
        an ID.
        """
        entry = get_generic_answer()
        entry.formId = TestEntryRouterNotAuthenticated.formId

        response = self.client.post(
            "/api/entry/create",
            json=entry.dict()
        )

        # we should get 200
        self.assertEqual(response.status_code, 200)

        # we should get a valid id
        self.assertTrue(response.json()["entryId"].startswith("entry-"))

    def test_submit_new_entry_and_retrieve_it(self):
        """
        Try like in test_submit_new_entry to make a new entry
        and then try to retrieve it
        """
        entry = get_generic_answer()
        entry.formId = TestEntryRouterNotAuthenticated.formId
        response = self.client.post(
            "/api/entry/create",
            json=entry.dict()
        )
        # we should get 200
        self.assertEqual(response.status_code, 200)
        # we should get a valid id
        self.assertTrue(response.json()["entryId"].startswith("entry-"))
        returned_id = response.json()["entryId"]

        response = self.client.get(
            f"/api/entry/view-entry/{returned_id}"
        )

        # we should get back our entry
        self.assertEqual(response.status_code, 200)
        entry = smart_forms_types.FormAnswer(
            **response.json()
        )
        self.assertEqual(entry.answerId, returned_id)
        self.assertIsNotNone(entry.creationDate)

    def test_submit_new_entry_and_delete_it(self):
        """
        Try like in test_submit_new_entry to make a new entry
        and then try to retrieve it
        """
        entry = get_generic_answer()
        entry.formId = TestEntryRouterNotAuthenticated.formId

        response = self.client.post(
            "/api/entry/create",
            json=entry.dict()
        )
        # we should get 200
        self.assertEqual(response.status_code, 200)
        # we should get a valid id
        self.assertTrue(response.json()["entryId"].startswith("entry-"))
        returned_id = response.json()["entryId"]

        response = self.client.delete(
            f"/api/entry/delete/{returned_id}"
        )
        # we should get 200
        self.assertEqual(response.status_code, 200)

        # try to get the deleted form
        response = self.client.get(
            f"/api/entry/view-entry/{returned_id}"
        )
        # we should get 400
        self.assertEqual(response.status_code, 201)

    
    def test_submit_new_entry_and_edit_it(self):
        """
        Try like in test_submit_new_entry to make a new entry
        and then try to retrieve it
        """
        entry = get_generic_answer()
        entry.formId = TestEntryRouterNotAuthenticated.formId

        entry.answers[0] = 'x' + entry.answers[0][1:]
        response = self.client.post(
            "/api/entry/create",
            json=entry.dict()
        )
        # we should get 200
        self.assertEqual(response.status_code, 200)
        # we should get a valid id
        self.assertTrue(response.json()["entryId"].startswith("entry-"))
        returned_id = response.json()["entryId"]

        # update the entry
        entry.answerId = returned_id
        entry.answers[0] = 'y' + entry.answers[0][1:]
        response = self.client.put(
            f"/api/entry/edit",
            json=entry.dict()
        )
        # we should get 200
        self.assertEqual(response.status_code, 200)

        # try to get the updated form
        response = self.client.get(
            f"/api/entry/view-entry/{returned_id}"
        )
        # we should get 200
        self.assertEqual(response.status_code, 200)

        # we should get back our modified entry
        self.assertEqual(response.status_code, 200)
        entry = smart_forms_types.FormAnswer(
            **response.json()
        )
        self.assertEqual(entry.answers[0][0], 'y')


    
    def test_view_entries(self):
        """
        Try like in test_submit_new_entry to make a new entry
        and then try to retrieve it
        """
        entry = get_generic_answer()
        entry.formId = TestEntryRouterNotAuthenticated.formId
        
        response = self.client.post(
            "/api/entry/create",
            json=entry.dict()
        )
        # we should get 200
        self.assertEqual(response.status_code, 200)
        # we should get a valid id
        self.assertIsNotNone(response.content)
        self.assertTrue(response.json()["entryId"].startswith("entry-"))
        returned_id = response.json()["entryId"]

        response = self.client.post(
            f"/api/entry/view-form-entries",
            json={
                "formId": TestEntryRouterNotAuthenticated.formId,
                "offset": 0,
                "count": 100
            }
        )

        # we should get 200
        self.assertEqual(response.status_code, 200)
        entries = response.json()

        self.assertGreaterEqual(entries["totalFormsCount"], 1)
        entry = [i for i in entries["entries"] if i["answerId"] == returned_id]

        self.assertNotEqual(entry, [])

if __name__ == '__main__':
    unittest.main()
    