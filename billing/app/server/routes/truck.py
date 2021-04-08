# ------- 3rd party imports -------
from flask import Blueprint, request
from app.server.db.models import *
from app.server.db.helper import helper

# ------- local imports -------
truck_blueprint = Blueprint('truck_blueprint', __name__)


@truck_blueprint.route("/truck", methods=['POST', 'PUT', 'GET'])
def truck():
    if request.method == 'POST':
        args = request.args
        provider_name = args.get('provider_name')
        truck_id = args.get('truck_id')

        if provider_name and truck_id:
            queried_provider = helper.get_one(Provider, name=provider_name)


    elif request.method == 'PUT':
        pass
        
    elif request.method == 'GET':
	    pass

