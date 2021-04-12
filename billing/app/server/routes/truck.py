# ------- 3rd party imports -------
from flask import Blueprint, request
from app.server.db.models import *
from app.server.db.helper import helper

# ------- local imports -------
truck_blueprint = Blueprint('truck_blueprint', __name__)


@truck_blueprint.route("/truck", methods=['POST', 'PUT', 'GET'])
def truck():
    if request.method == 'POST':

        provider_id = (request.form and request.form["provider_id"]) or (request.json and request.json.get("provider_id"))
        truck_id = (request.form and request.form["truck_id"]) or (request.json and request.json.get("truck_id"))

        queried_provider = helper.get_one(Provider, id=provider_id)

        if queried_provider and truck_id:
            helper.add_instance(Truck,
                                truck_id=truck_id,
                                provider_id=queried_provider.id)
            return 'truck was added successfully'

        elif not queried_provider:
            return 'Provider was not found'

        elif not truck_id:
            return 'Please provide a valid truck ID'


@truck_blueprint.route("/test")
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
