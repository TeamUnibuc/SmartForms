import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

import unittest
import main
import main
from fastapi.testclient import TestClient

class TestStatisticsEndpoint(unittest.TestCase):
    def setUpClass() -> None:
        main.init_state()
        
    def test_global_statistics_endpoint(self):
        client = TestClient(main.app)
        response = client.get("/api/statistics/global")
        self.assertEqual(response.status_code, 200)        

if __name__ == '__main__':
    unittest.main()