# ------- 3rd party imports -------
from flask import Blueprint, request, jsonify
from app.server.db.models import *
from app.server.db.helper import helper
from datetime import datetime
import json

# ------- local imports -------
bill_blueprint = Blueprint('bill_blueprint', __name__)


@bill_blueprint.route("/bill/<id>", methods=['GET'])
def bill(id):
	provider = helper.get_one(Provider, id=id)
	if provider is None:
		return "no such provider", 400
		
		now = datetime.now()	
		from_default = now.strftime('%Y%m') +'01000000'
		to_default = now.strftime('%Y%m%d%H%M%S')
		
		from_arg = request.args.get('from')
		if not from_arg:
			from_arg = from_default
		else:
			if len(from_arg) != 14:
				return "wrong datetime value"
			try:
				datetime(from_arg[0:4], from_arg[4:6], from_arg[6:8], from_arg[8:10], from_arg[10:12], from_arg[12:14])
			except(ValueError):
				return "wrong datetime value"
				
		to_arg = request.args.get('to')
		if not to_arg:
			to_arg = to_default
		else:
			if len(to_arg) != 14:
				return "wrong datetime value"
			try:
				datetime(to_arg[0:4], to_arg[4:6], to_arg[6:8], to_arg[8:10], to_arg[10:12], to_arg[12:14])
			except(ValueError):
				return "wrong datetime value"
	
	mocked_json=json.dumps ({
		"id": provider.id,
		"name": provider.name,
		"from": from_arg,
		"to": to_arg,
		"truckCount": 0,
		"sessionCount": ,
		"products": [
			{ "product": "orange",
				"count": 5, 
				"amount": 500, 
				"rate": 100, 
				"pay": 50000
			},
			{ "product": "mandarina",
				"count": 3, 
				"amount": 300, 
				"rate": 200, 
				"pay": 60000
			},
		],
		"total": 110000
	})
	
	return mocked_json
    
    
