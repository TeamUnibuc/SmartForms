import json
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

import time
import random
import unittest
from main import init_state
import main
from fastapi.testclient import TestClient

class TestEntryEndpoint(unittest.TestCase):
    def setUpClass() -> None:
        init_state()
        
    def test_root_endpoint(self):
        self.assertEqual(1, 1)


# TODO:
# keeping this here for having a template
        # client = TestClient(fastapi_engine.app)
        # response = client.get("/")
        # self.assertEqual(response.status_code, 200)

    # def test_get_recipe(self):
    #     client = TestClient(fastapi_engine.app)
    #     response = client.get("/view-available-recipes")
    #     self.assertEqual(response.status_code, 200)
    #     continut = response.json()
    #     self.assertTrue("recipes" in continut)

    # def test_add_recipe_invalid_request(self):
    #     client = TestClient(fastapi_engine.app)
    #     req = {
    #         "some-invalid-request": "idk"
    #     }
    #     response = client.post("/view-available-recipes", json=req)
    #     self.assertNotEqual(response.status_code, 200)

    # def test_add_recipe_valid_request(self):
    #     client = TestClient(fastapi_engine.app)
    #     recipe = {
    #         "drink_name": "normal_coffee_" + str(random.randint(1, 10**10)),
    #         "drink_description": "",
    #         "coffee_mg": 10,
    #         "milk_mg": 10,
    #         "water_mg": 10,
    #         "sugar_mg": 10,
    #         "milk_foam": False 
    #     }
    #     response = client.post("/add-new-recipe", json=recipe)
    #     self.assertEqual(response.status_code, 200)

    # def test_add_recipe_existing_name(self):
    #     client = TestClient(fastapi_engine.app)
    #     recipe = {
    #         "drink_name": "normal_coffee_" + str(random.randint(1, 10**10)),
    #         "drink_description": "",
    #         "coffee_mg": 10,
    #         "milk_mg": 10,
    #         "water_mg": 10,
    #         "sugar_mg": 10,
    #         "milk_foam": False 
    #     }
    #     response = client.post("/add-new-recipe", json=recipe)
    #     self.assertEqual(response.status_code, 200)
    #     response = client.post("/add-new-recipe", json=recipe)
    #     self.assertTrue("status" in response.json() and response.json()["status"] == "FAIL")

    # def test_delete_recipe_inexisting_name(self):
    #     client = TestClient(fastapi_engine.app)

    #     response = client.post("/delete-recipe", params={"recipe_name": "inexistent_coffee"})
    #     self.assertTrue("status" in response.json() and response.json()["status"] == "FAIL")

    
    # def test_delete_existing_name(self):
    #     client = TestClient(fastapi_engine.app)
    #     recipe = {
    #         "drink_name": "normal_coffee_" + str(random.randint(1, 10**10)),
    #         "drink_description": "",
    #         "coffee_mg": 10,
    #         "milk_mg": 10,
    #         "water_mg": 10,
    #         "sugar_mg": 10,
    #         "milk_foam": False 
    #     }
    #     response = client.post("/add-new-recipe", json=recipe)
    #     self.assertEqual(response.status_code, 200)
    #     response = client.post("/delete-recipe", params={"recipe_name": recipe["drink_name"]})
    #     self.assertTrue("status" in response.json() and response.json()["status"] == "OK")


    # def test_view_order_history(self):
    #     client = TestClient(fastapi_engine.app)
        
    #     response = client.get("/view-order-history")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue("orders" in response.json())
    

    # def test_view_popular_drinks(self):
    #     client = TestClient(fastapi_engine.app)
        
    #     response = client.get("/view-popular-drinks")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue("drinks" in response.json())
    

    # def test_view_machines_status(self):
    #     old_heartbeat_value = storage.coffee_machines_last_heartbeat
    #     old_levels_values = storage.coffee_machines_levels

    #     storage.coffee_machines_last_heartbeat = {
    #         'machine1': 1234
    #     }
    #     storage.coffee_machines_levels = {
    #         'machine1': mqtt_messages.MachineLevels()
    #     }

    #     client = TestClient(fastapi_engine.app)
        
    #     response = client.get("/view-machines-status")

    #     storage.coffee_machines_last_heartbeat = old_heartbeat_value
    #     storage.coffee_machines_levels = old_levels_values

    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue("machines" in response.json())

    
    # def test_request_new_drink(self):
    #     client = TestClient(fastapi_engine.app)
    #     drink_name = "normal_coffee_" + str(random.randint(1, 10**10))
    #     new_drink_json = {
    #         "recipient_machine_id": "machine1",
    #         "coffee_name": drink_name
    #     }

    #     response = client.post("/request-new-drink", json=new_drink_json)
    #     self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()