# ------- standard library imports -------
import json
import unittest

# ------- local imports -------
import requests
from flask import request

from app.server.db.extensions import db
from app.server.db.models import *
from app.app import create_app
from app.tests.api_testing.api_test_helper import ApiTestHelper
from app.server.db.helper import helper


class TestApp(unittest.TestCase):
    TRUCK_ENDPOINT = '/truck'

    def setUp(self):
        self.app = create_app(config_file='settings.py')
        self.helper = ApiTestHelper()
        with self.app.test_request_context():
            self.base_url = request.base_url

    def test_add_truck(self):
        self.helper.add_instance_to_provider('tomer')
        res = requests.post('http://127.0.0.1:5000/truck',
                            params={'provider_name': 'tomer', 'truck_id': '44'})
        print(res.text)

    def tearDown(self):
        db.session.remove()
        with self.app.app_context():
            db.drop_all()


if __name__ == '__main__':
    test = TestApp()
