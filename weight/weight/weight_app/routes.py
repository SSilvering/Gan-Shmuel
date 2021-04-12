from weight_app import weight_app, requests, GETweight, POSTweight, GETunknown, GETitem, GEThealth, GETsession
from time import gmtime, strftime
from datetime import datetime
from flask import request, jsonify,render_template
import mysql.connector
from . import weight_app
from .POSTweight import POSTweight
from .GETweight import GETweight
from .GETitem import GETitem
from .GEThealth import GEThealth
from .GETunknown import unknown_func
from .GETsession import GETsession
from .db_module import DB_Module
import json, csv

@weight_app.route('/')
@weight_app.route('/index')
def index():
    return render_template('index.html')

@weight_app.route('/health', methods=['GET'])
def health_check():
    #a tuple of the all the apis that will be used in the project 
    return GEThealth()

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

@weight_app.route("/session")
def check_sesion():
    return "Hello there! Session is working"

@weight_app.route("/session/<id>")
def get_session(id="<id>"):
    return GETsession(id)

@weight_app.route('/weight', methods=['GET'])
def GETweight_route():
    currenttime = strftime("%Y%m%d%H%M%S", gmtime())
    start_of_day = strftime("%Y%m%d000000", gmtime())
    from_time = request.args.get('from', default = start_of_day, type = str)
    to_time = request.args.get('to', default = currenttime, type = str)
    filter_type = request.args.get('filter', default = '*', type = str)
    return GETweight(from_time,to_time,filter_type)

@weight_app.route('/item',methods=['GET'])
def get_only_item():
    return "Hello from Item!"
@weight_app.route('/item/<item_id>', methods=['GET'])
def GETitem_route(item_id):
    from_time = request.args.get('from')
    to_time = request.args.get('to')
    return GETitem(item_id,from_time,to_time)

@weight_app.route('/batch-weight', methods=['POST'])
def batch_weight():#author: Niv Yohanok

    filename = request.args.get('filename')
    filepath = f'./weight_app/in/{filename}'
    query_list = []

    # data = []
    is_csv = False
    query = f"INSERT INTO containers (id,weight,unit) VALUES (%s,%s,%s)"

    with open(filepath,'r') as my_file: #case if it's JSON
        try:
            data = json.load(my_file)
            for line in data:

                _id = line['id']
                weight = line['weight']
                unit = line['unit']
                values = (_id, weight,unit)

                query_list.append(values)

        except:
            is_csv = True


    if is_csv: #case if it's CSV
        with open(filepath,'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for line in reader:

                _id = list(line.values())[0]
                weight = list(line.values())[1]
                unit = list(line.keys())[1]
                values = (_id, weight,unit)

                query_list.append(values)

    retrived = ''
    db = DB_Module ()
    db.insert_new_data(query,query_list)
    retrived = db.fetch_new_data('SELECT * FROM containers')

    return jsonify(retrived)

@weight_app.route('/unknown', methods=['GET'])
def unknown_weight():
    return unknown_func()
