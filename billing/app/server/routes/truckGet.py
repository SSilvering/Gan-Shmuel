# ------- 3rd party imports -------
from flask import Blueprint, request, jsonify
from app.server.db.models import *
from app.server.db.helper import helper
from datetime import datetime
from requests.exceptions import HTTPError, ConnectionError
from json.decoder import JSONDecodeError

# ------- local imports -------
truckGet_blueprint = Blueprint('truckGet_blueprint', __name__)
import requests
from app.setup.settings import WEIGHT_URI


def get_truck_info(truck_id, from_arg, to_arg):
    try:
        response = requests.get(WEIGHT_URI + f'/item/{truck_id}',
                                params={'from': from_arg, 'to': to_arg})
        response.raise_for_status()
        return response
    except (HTTPError, ConnectionError) as err:
        print(f'Bad responce from WEIHGT server: {err}')
    return 'mocked get_sessions because of bad respone from WEIGHT server'


@truckGet_blueprint.route("/truck/<id>", methods=['GET'])
def truckGet(id):
    if request.method == 'GET':
        truck = helper.get_one(Truck, truck_id=id)
        if truck is None:
            return ('truck ID not exist', 404)
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

    try:
        truck_info = get_truck_info(truck.truck_id, from_arg, to_arg).json()
        return jsonify(id=truck.truck_id, tara=truck_info['tara'], sessions=truck_info['sessions'])
    except JSONDecodeError as json_error:
        return jsonify(id=truck.truck_id, tara=None, sessions=f'Json responce decoding error: {json_error}')
