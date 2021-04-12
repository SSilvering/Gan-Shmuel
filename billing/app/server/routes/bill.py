# ------- 3rd party imports -------
from flask import Blueprint, request, jsonify
from app.server.db.models import *
from app.server.db.helper import helper
from datetime import datetime
import json
from requests.exceptions import HTTPError, ConnectionError
from json.decoder import JSONDecodeError

# ------- local imports -------
bill_blueprint = Blueprint('bill_blueprint', __name__)
import requests
from app.setup.settings import WEIGHT_URI

DEFAULT_PRICE = 100


@bill_blueprint.route("/bill/<id>", methods=['GET'])
def bill(id):
	provider = helper.get_one(Provider, id=id)
	if provider is None:
		return "wrong provider id", 400

	now = datetime.now()
	from_default = now.strftime('%Y%m') + '01000000'
	to_default = now.strftime('%Y%m%d%H%M%S')

	from_arg = request.args.get('from')
	if not from_arg:
		from_arg = from_default

	else:
		if len(from_arg) != 14:
			return "wrong datetime value"
		try:
			datetime(from_arg[0:4], from_arg[4:6], from_arg[6:8], from_arg[8:10], from_arg[10:12], from_arg[12:14])
		except ValueError:
			return "wrong datetime value"

	to_arg = request.args.get('to')
	if not to_arg:
		to_arg = to_default
	else:
		if len(to_arg) != 14:
			return "wrong datetime value"
		try:
			datetime(to_arg[0:4], to_arg[4:6], to_arg[6:8], to_arg[8:10], to_arg[10:12], to_arg[12:14])
		except ValueError:
			return "wrong datetime value"

	mocked_json = json.dumps({
        "id": 'BAD RESPONSE FROM WEIGHT SERVER',
        "name": provider.name,
        "from": from_arg,
        "to": to_arg,
        "truckCount": 0,
        "sessionCount": 0,
        "products": [
            {"product": "orange",
             "count": 5,
             "amount": 500,
             "rate": 100,
             "pay": 50000
             },
            {"product": "mandarina",
             "count": 3,
             "amount": 300,
             "rate": 200,
             "pay": 60000
             },
        ],
        "total": 110000
    })
		
	#1 - get list of truck_id references to provider.id
	#2 - for every truck, request get item (truck_id, from, to)   
	#3 - count amount of non-empty json['sessions'] responces =>truckCount
	#4 - get sessions list from these responces: sessions = [ses1, ses2, ...]
	#5 - len(sessions) => sessionsCount
	#6 - for every session, count (with dict) products= {product_id1:(number of session with this product_id, total neto weight)}
	#7 - search for price, first check Rates(product_id, provider.id) for rate, if not found - only Rates(product_id) (All scope)
	#8 - pay = amount*rate
	#9 - total = sum(products['pay']) 
	
	#1
	trucks = helper.get_all_with_filter(Truck, provider_id=provider.id)
	#2
	try:
		truckCounter = 0
		sessionCounter = 0
		sessions =[]
		for truck in trucks:
			truck_id=truck.truck_id
			response = requests.get(WEIGHT_URI + f'/item/{truck_id}',
									params={'from': from_arg, 'to': to_arg})
			response.raise_for_status()
			truck_sessions = response.json()['sessions']
	#3
			if len(truck_sessions) > 0:
				truckCounter += 1
	#5
			sessionCounter += len(truck_sessions)
	#4
			for session in truck_sessions:
				sessions.append(session)
		products = dict()
	#6
		for session in sessions:
			repsonse = requests.get(WEIGHT_URI + 'f/session/{session}')
			response.raise_for_status()
			session_data = response.json()
			product_id = session_data['product_id']
			#session counter, total neto weight, price (rate) and pay
			products.setdefault(product_id, [0,0,0,0])
			products[product_id][0] += 1
			if session_data['neto'].isdigit():
				products[product_id][1] += session_data['neto']
	#7
		for product_name, product_data in products.items():
			price = helper.get_one(Rate, product_name=product_name, provider_id=provider.id)
			if price is None:
				price = helper.get_one(Rate, product_name=product_name)
			if price is None:
	#NOTIFY USER THAT PRICE OF product_id IS MISSING IN DB
				price = DEFAULT_PRICE
			product_data[2] = price
	#8, 9
		total = 0
		for product_name, product_data in products.items():
			pay = product_data[1] * product_data[2]
			product_data[3] = pay
			total += pay
			
		products_output = list()
		for product_name, product_data in products.items():
			products_output.append({ "product": product_name,
									"count": product_data[0], #number of sessions
									"amount": product_data[1], #total kg
									"rate": product_data[2], #agorot
									"pay": product_data[3] #agorot
									})
		output_json = json.dumps({
			"id": provider.id,
			"name": provider.name,
			"from": from_arg,
			"to": to_arg,
			"truckCount": truckCounter,
			"sessionCount": sessionCounter,
			"products": products_output,
			"total": total
		})
    
		return output_json
    
	except (HTTPError, ConnectionError, JSONDecodeError):
		return mocked_json
		
	
#	return mocked_json
