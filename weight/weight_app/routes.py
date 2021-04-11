
from weight_app import weight_app, requests, GETweight, POSTweight
from time import gmtime, strftime
from datetime import datetime
from flask import request
import mysql.connector
from . import weight_app
from .GETweight import GETweight
from .POSTweight import POSTweight
from .get_item import get_sql
from .db_module import DB_Module
import json



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
    
@weight_app.route('/session')
@weight_app.route('/session/<id>')
def get_session(id="<id>"):
    if id is not None:
        #select_query = f"SELECT id, trucks_id, bruto, neto FROM sessions where trucks_id={id}"
         
        select_query = f"SELECT t1.id, t1.trucks_id, t1.bruto, t1.neto, t2.weight FROM sessions t1, trucks t2 WHERE t1.trucks_id = {id} and t1.trucks_id = t2.truckid"
        tags = ('id', 'trucks_id', 'bruto', 'neto')
        db = DB_Module ()
        data = db.fetch_new_data(select_query)
        print(type(data))
        session = dict()
        for ind in range(0, len(data)):
            session[tags[ind]] = data[ind]
        return json.dumps(session)
    return "provide a truck ID"


@weight_app.route('/weight', methods=['GET'])
def GETweight_startup():
    currenttime = strftime("%Y%m%d%H%M%S", gmtime())
    start_of_day = strftime("%Y%m%d000000", gmtime())
    from_time = request.args.get('from', default = start_of_day, type = str)
    to_time = request.args.get('to', default = currenttime, type = str)
    filter_type = request.args.get('filter', default = '*', type = str)
    #db_name = "weight_testing_db"
    return GETweight(from_time,to_time,filter_type)
    #return "Hello from GET/weight!"
#=======================
#=======================



@weight_app.route('/item')
@weight_app.route('/item/<id>', methods=['GET'])
def get_item(id):
    from_time = request.args.get('from')
    to_time = request.args.get('to')

    if not from_time:
        from_time = datetime.now().strftime("%Y-%m-01 00:00:00")
    if not to_time:
        to_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # print (f'start time: {from_time} end time: {to_time}')
    query = f"SELECT (bruto,neto,id) from sessions WHERE date BETWEEN {from_time} AND {to_time}"

    
