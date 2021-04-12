from flask_testing import TestCase
from app.setup.setup import create_app
import unittest
from app.server.db.models import *
# from app.server.db.models import *
from os import path
from app.server.db.helper import helper


class MyTest(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///testingdb.db"
    TESTING = True

    def create_app(self):
        self.app = create_app(f'{path.dirname(path.realpath(__file__))}/settings.py')
        return self.app
        # return create_app(config_file=f'{path.dirname(path.realpath(__file__))}/settings.py')

    def test_post_rates(self):
        print("testing empty post ...")
        with self.app.test_client() as c:
            resp = c.post('/rates')
            self.assert_400(resp, "Fail: empty post request")

    def test_post_nonexist_file_rates(self):
        print("testing malformed parameters for post ...")
        with self.app.test_client() as c:
            resp = c.post('/rates', data=dict(file="thereisnopossibilitythisfilenameexistsontheserver.yy"))
            self.assert_400(resp, "Fail: post request with wrong params")

    def test_correct_post_rates(self):
        print("testing post request with known file in the server ...")
        with self.app.test_client() as c:
            resp = c.post('/rates', data=dict(file="rates.xlsx"))
            self.assert_200(resp, "Fail: post request with correct params")

    def setUp(self):
        pass
        # db.create_all()

    def tearDown(self):
        db.session.remove()
        with self.app.app_context():
            db.drop_all()


print("hello world")
test = MyTest()
