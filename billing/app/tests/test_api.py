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
    TRUCK_ENDPOINT = 'truck'

    def setUp(self):
        self.app = create_app(config_file='settings.py')
        self.helper = ApiTestHelper()

        with self.app.test_request_context():
            self.base_url = request.host
            self.provider1 = helper.add_instance(Provider, name='tomer')

    def test_add_truck_succeeds(self):
        truck_path = f'http://localhost:5000/truck'
        params = {
            'provider_name': 'tomer',
            'truck_id': '1234'
        }
        res = requests.post(truck_path, params=params)
        self.assertEqual(res.text, 'truck was added successfully')

    def test_add_truck_fail_no_provider(self):
        truck_path = f'http://localhost:5000/truck'
        params = {
            'provider_name': 'john',
            'truck_id': '1234'
        }
        res = requests.post(truck_path, params=params)
        self.assertEqual(res.text, 'Provider was not found')

    def test_add_truck_fail_no_truck_id(self):
        truck_path = f'http://localhost:5000/truck'
        params = {
            'provider_name': 'tomer',
        }
        res = requests.post(truck_path, params=params)
        self.assertEqual(res.text, 'Please provide a valid truck ID')

    def tearDown(self):
        db.session.remove()
        with self.app.app_context():
            db.drop_all()


if __name__ == '__main__':
    test = TestApp()
