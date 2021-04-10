from weight_app import weight_app, requests, POSTweight
from time import gmtime, strftime
from flask import request
import mysql.connector
from . import weight_app
from .POSTweight import POSTweight
#from get_weight import get_weight

@weight_app.route('/')
@weight_app.route('/index')
def index():
    return "Hello, World!"


@weight_app.route('/health', methods=['GET'])
def health_check():
    #a tuple of the all the apis that will be used in the project 
    api_tuple = ("index","batch-weight","unknown","item","session","post","weight")
    for item in api_tuple:
        uri = f"http://localhost:8080/{item}"
        req = requests.get(uri)
        print(req.status_code)
        if req.status_code < 200 or req.status_code > 299:
            res = f"APP Status is {req.status_code}"
            return res
    return f"APP status is {req.status_code}"


@weight_app.route('/weight', methods=['POST'])
def post_weight():
    direction = request.args.get('direction')
    truck = request.args.get('truck', "na")
    containers = request.args.get('containers', None)
    weight = request.args.get('weight', None)
    weight_type = request.args.get('unit')
    force = request.args.get('force', None)
    produce = request.args.get('produce', None)

    return POSTweight(direction, truck, containers, weight, weight_type, force, produce)
    
    
