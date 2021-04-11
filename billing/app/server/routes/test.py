# ------- 3rd party imports -------
from flask import Blueprint
from app.server.db.models import *
from app.server.db.helper import helper

# ------- local imports -------
test_blueprint = Blueprint('test_blueprint', __name__)


@test_blueprint.route("/test1")
def test1():
    # helper.add_instance(Provider, name="provider1")
    # helper.add_instance(Provider, name="provider2")
    # helper.add_instance(Rate, product_name="potatoes", rate=350, scope='ALL')
    # helper.add_instance(Rate, product_name="cucumbers", rate=290, scope='ALL')
    # provider1_id = helper.get_one(Provider, name="provider1").id
    # helper.add_instance(Rate, product_name="red_orange", rate=990, scope=provider1_id)
    # return str(provider1_id)

    # helper.add_instance(Truck, truck_id="123ABC",weight=250, provider_id=1)
    truck1 = helper.get_one(Truck, truck_id='123ABC')
    return str(truck1)


@test_blueprint.route("/")
def index():
    return 'Billing system is up', 200


@test_blueprint.route("/test")
def test():
    provider1 = helper.add_instance(Provider,
                                    name=tomer)

    rate1 = helper.add_instance(Rate,
                                product_name='cucumba',
                                rate=200,
                                scope=provider1.id)

    truck1 = helper.add_instance(Truck,
                                 truck_id='1234',
                                 provider_id=provider1.id)
    return 'Hello!'
