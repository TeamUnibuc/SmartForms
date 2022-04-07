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

class TestFormExtractor(unittest.TestCase):
    def setUpClass() -> None:
        init_state()

