from flask_testing import TestCase
from app.setup.setup import create_app
import unittest
from app.server.db.models import *
from os import path
from app.server.db.helper import helper
import sys


class TruckTest(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///testingdb.db"
    TESTING = True

    def create_app(self):
        self.app = create_app(path.dirname(path.realpath(__file__))+'/settings.py')
        return self.app
        # return create_app(config_file=f'{path.dirname(path.realpath(__file__))}/settings.py')

    def test_put_nonexist_provider_id(self):
        #sys.stdout.write("testing put request without provider_id param ...")
        tid = "noclue"
        helper.add_instance(Truck, id=6, truck_id=tid, weight=500.5, provider_id=10)
        helper.commit_changes()
        with self.app.test_client() as c:
            resp = c.put(f'/truck/{tid}')
            #sys.stdout.write("response: ", resp.data)
            self.assert_400(resp, "Fail:  put request without provider_id param")

    def test_put_nonexist_truck_id(self):
        tid = "foo"
        truck = helper.get_one(Truck, truck_id=tid)
        if truck is not None:
            db.session.remove(truck)
            helper.commit_changes()
        #sys.stdout.write("testing put request with truck_id not found in truck table ...")

        with self.app.test_client() as c:
            resp = c.put(f'/truck/{tid}')
            #sys.stdout.write("response: " + resp.data)
            self.assert_400(resp, "Fail: put request with nonexistent truck param")

    def test_put_nonexistent_new_prov_id_in_providers(self):
        tid = "moo"
        pid = 10
        helper.add_instance(Truck, id=6, truck_id=tid, weight=500.5, provider_id=pid)
        # helper.add_instance(Provider,id=pid,name="hanks")
        helper.commit_changes()
        #sys.stdout.write("testing truck put request with new id that is not found in the providers table...")

        with self.app.test_client() as c:
            resp = c.put(f'/truck/{tid}', data=dict(provider_id=15))
            #sys.stdout.write("response: " + resp.data)
            self.assert_400(resp, "Fail: put request with nonexistent new_provider_id in providers table")

    def test_put_correct_request(self):
        tid = "too"
        pid = 20
        new_pid = 30
        helper.add_instance(Truck, id=6, truck_id=tid, weight=500.5, provider_id=pid)
        helper.add_instance(Provider, id=pid, name="john")
        helper.add_instance(Provider, id=new_pid, name="mario")
        helper.commit_changes()
        #sys.stdout.write("testing correct truck put request ...")

        with self.app.test_client() as c:
            resp = c.put(f'/truck/{tid}', data=dict(provider_id=new_pid))
            #sys.stdout.write("response: " + resp.data)
            self.assert_200(resp, "Fail: put request with correct request info")

    def tearDown(self):
        pass
        db.session.remove()
        with self.app.app_context():
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
    # test = TruckTest()
