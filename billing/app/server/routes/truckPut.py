# ------- 3rd party imports -------
from flask import Blueprint, request
from app.server.db.models import *
from app.server.db.helper import helper

# ------- local imports -------
truckPut_blueprint = Blueprint('truckPut_blueprint', __name__)


@truckPut_blueprint.route("/truck/<id>", methods=['PUT'])
def truckPut(id):
	truck_id = helper.get_one(Truck, truck_id=id)
	if truck_id is None:  # unacceptable parameter
		return "the <id> sent isn't related to any existing entry on the server\n", 406

	new_prov_id = request.form and request.form["provider_id"] or request.json and request.json.get("provider_id")
	if not new_prov_id.isnumeric() or helper.get_one(Provider, id=int(new_prov_id)) is None:
		return 'invalid or non existing provider linked with this id\n', 406
	truck_id.provider_id = new_prov_id
	helper.commit_changes()
	return 'OK\n', 200
