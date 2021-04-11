# ------- 3rd party imports -------
from flask import Blueprint, request
from app.server.db.models import *
from app.server.db.helper import helper

# ------- local imports -------
truck_blueprint = Blueprint('truck_blueprint', __name__)


@truck_blueprint.route("/truck", methods=['POST'])
def truck():
    if request.method == 'POST':

        args = request.args
        provider_name = args.get('provider_name')
        truck_id = args.get('truck_id')

        queried_provider = helper.get_one(Provider, name=provider_name)

        if queried_provider and truck_id:
            helper.add_instance(Truck,
                                truck_id=truck_id,
                                provider_id=queried_provider.id)
            return 'truck was added successfully'

        elif not queried_provider:
            return 'Provider was not found'

        elif not truck_id:
            return 'Please provide a valid truck ID'
