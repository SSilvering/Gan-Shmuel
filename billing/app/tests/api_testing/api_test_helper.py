from flask import Blueprint, request
from app.server.db.models import *
from app.server.db.helper import helper
from app.app import app


class ApiTestHelper:

    @staticmethod
    def populate_db(
            provider_name: str,
            product_name: str,
            truck_id: str):

        with app.app_context():
            provider1 = helper.add_instance(Provider,
                                            name=provider_name)

            rate1 = helper.add_instance(Rate,
                                        product_name=product_name,
                                        rate=200,
                                        scope=provider1.id)

            truck1 = helper.add_instance(Truck,
                                         truck_id=truck_id,
                                         provider_id=provider1.id)


