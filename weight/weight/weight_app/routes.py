from weight_app import weight_app, requests, GETweight, POSTweight
from time import gmtime, strftime
from datetime import datetime
from flask import request, jsonify
import mysql.connector
from . import weight_app
from .POSTweight import POSTweight
from .GETweight import GETweight
from .db_module import DB_Module
import json, csv

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

@weight_app.route("/session")
@weight_app.route("/session/<id>")
def get_session(id="<id>"):
    if id is not None:
        select_query = f"SELECT t1.id, t1.trucks_id, t1.bruto, \
            CASE WHEN t1.direction = 'out' then (select t1.bruto-t1.neto AS 'truckTara' FROM sessions t1, \
                trucks t2 WHERE t1.id = {id} and t1.trucks_id = t2.truckid ) end tara, t1.neto FROM \
                sessions t1, trucks t2 WHERE t1.id = {id} and t1.trucks_id = t2.truckid"
        
        db = DB_Module ()
        query = f"select direction from sessions where id={id}"
        data = db.fetch_new_data(query)
        for item in data:
            if item['direction'] == 'out':
                select_query = f"SELECT t1.id, t1.trucks_id, t1.bruto, t1.bruto-t1.neto AS 'truckTara', t1.neto, t1.products_id FROM sessions t1, trucks t2 WHERE t1.id = {id} and t1.trucks_id = t2.truckid"
            else:
                select_query = f"SELECT t1.id, t1.trucks_id, t1.bruto, t1.products_id FROM sessions t1, \
                    trucks t2 WHERE t1.id = {id} and t1.trucks_id = t2.truckid"
        data = db.fetch_new_data(select_query)
        session = []
        #for ind in range(0, len(data)):
        for res in data:
            session.append(res)
        return jsonify(session)
        
    return "provide a truck ID"

@weight_app.route('/weight', methods=['GET'])
def GETweight_startup():
    currenttime = strftime("%Y%m%d%H%M%S", gmtime())
    start_of_day = strftime("%Y%m%d000000", gmtime())
    from_time = request.args.get('from', default = start_of_day, type = str)
    to_time = request.args.get('to', default = currenttime, type = str)
    filter_type = request.args.get('filter', default = '*', type = str)
    return GETweight(from_time,to_time,filter_type)
#=======================
#=======================

@weight_app.route('/item')
def get_only_item():
    return "Hello from Item!"
@weight_app.route('/item/<item_id>', methods=['GET'])
def get_item(item_id):

    from_time = request.args.get('from')
    to_time = request.args.get('to')

    data = []
    session = { #basic mold for the return object
        "id":int(item_id),
        "tara":0,
        "sessions":[]
    }

    if not from_time: #default cases for time 
        from_time = datetime.now().strftime("%Y%m01000000")
    if not to_time:
        to_time = datetime.now().strftime("%Y%m%d%H%M%S")

    query = f"SELECT bruto,neto,id,date FROM sessions WHERE id={item_id} AND date BETWEEN {from_time} AND {to_time}"

    try:
        db = DB_Module ()
        data = db.fetch_new_data(query)
    except:
        print ("mysql has failed to reach the server..")

    
    if not data: #error case 
        session["id"] = 404,
        session["tara"] = 'N/A'

    for ind in range(0, len(data)):
        session["tara"] += float(data[ind]["bruto"]) - float(data[ind]["neto"])
        session["sessions"].append(data[ind]["id"])

    return jsonify(session)

@weight_app.route('/batch-weight', methods=['POST'])
def batch_weight():

    filepath = '/home/niv/Documents/Gan-Shmuel/weight/weight_app/in/containers2.csv'
    # filepath = '/home/niv/Documents/Gan-Shmuel/weight/weight_app/in/containers3.json'
    query_list = []
    data = []
    is_csv = False
    
    try: 
        db = DB_Module ()
        data = db.fetch_new_data(query)
    except:
        return "Failed to connect to database"
        
    with open(filepath,'r') as my_file: #case if it's JSON
        try:
            data = json.load(my_file)
        except:
            is_csv = True

    
    if is_csv: #case if it's CSV
        with open(filepath,'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for line in reader:
                _id = list(line.values())[0]
                weight = list(line.values())[1]
                unit = list(line.keys())[1]

                query = f"INSERT INTO containers (id,weight,unit) VALUES ({_id},{weight},{unit})"
                query_list.append(query)
    
    #execute queries

    return "FUCK"

@weight_app.route('/unknown', methods=['GET'])
def unknown_weight():
    query= "SELECT distinct id FROM containers WHERE weight IS NULL"
    try:
        db = DB_Module ()
       
    except:
        print("my sql has failed for some weird reason :(")
    print("connected")
    #id_container = []
    try:
        data = db.fetch_new_data(query) #sent to db the object querry and read it fadi make it =]
        
        return ' '.join([str(elem) for elem in data])
        
    except:
        print("my sql has failed for some weird reason :("), quit()
    return "no unkown weights"
