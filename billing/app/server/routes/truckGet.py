# ------- 3rd party imports -------
from flask import Blueprint, request, jsonify
from app.server.db.models import *
from app.server.db.helper import helper
from datetime import datetime, date
from requests.exceptions import HTTPError, ConnectionError

# ------- local imports -------
truckGet_blueprint = Blueprint('truckGet_blueprint', __name__)
import requests
from app.setup.settings import WEIGHT_STAGING_URI

def get_sessions(truck_id, from_arg, to_arg):
	try:
		response = requests.get(WEIGHT_STAGING_URI+f'/item/{truck_id}',
			params={'from': from_arg, 'to': to_arg})
		response.raise_for_status()
		return response.json()['sessions']
	except (HTTPError, ConnectionError) as err:
		print(f'Bad responce from WEIHGT server: {err}')  
	return 'mocked get_sessions because bad respone from WEIGHT server'
	


@truckGet_blueprint.route("/truck/<id>", methods=['GET'])
def truckGet(id):
	if request.method == 'GET':
		truck = helper.get_one(Truck, truck_id=id)
		if truck is None:
			return 'truck ID not exist', 404
		from_default = datetime(date.today().year, date.today().month, 1, 00, 00, 00)
		
		from_arg = request.args.get('from')
		if not from_arg:
			from_arg = from_default
		else:
			if len(from_arg) != 14:
				return "wrong datetime value"
			try:
				from_arg = datetime(from_arg[0:4], from_arg[4:6], from_arg[6:8], from_arg[8:10], from_arg[10:12], from_arg[12:14])
			except(ValueError):
				return "wrong datetime value"
				
		to_arg = request.args.get('to')
		if not to_arg:
			to_arg = datetime.now()
		else:
			if len(to_arg) != 14:
				return "wrong datetime value"
			try:
				to_arg = datetime(to_arg[0:4], to_arg[4:6], to_arg[6:8], to_arg[8:10], to_arg[10:12], to_arg[12:14])
			except(ValueError):
				return "wrong datetime value"
				
	return jsonify(id=truck.truck_id, tara=truck.weight, sessions=get_sessions(truck.truck_id, from_arg, to_arg))
