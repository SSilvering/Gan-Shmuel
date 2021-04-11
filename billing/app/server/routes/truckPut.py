# ------- 3rd party imports -------
from flask import Blueprint
from app.server.db.models import *
from app.server.db.helper import helper

# ------- local imports -------
truckPut_blueprint = Blueprint('truckPut_blueprint', __name__)


@truckPut_blueprint.route("/truck/<id>", methods=['PUT'])
def truckPut():
	if request.method == 'PUT':
		pass
	return 'not implemented yet', 200
