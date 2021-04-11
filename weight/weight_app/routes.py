
from weight_app import weight_app, requests, GETweight
from time import gmtime, strftime
from flask import request
import mysql.connector
from . import weight_app
from .GETweight import GETweight

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
    

@weight_app.route('/session')
@weight_app.route('/session/<id>')
def get_session(id="<id>"):
    return "Session"
@weight_app.route('/weight', methods=['GET'])
def GETweight_startup():
    currenttime = strftime("%Y%m%d%H%M%S", gmtime())
    print("currenttime = %s" % currenttime)
    start_of_day = strftime("%Y%m%d000000", gmtime())
    print("start_of_day = %s" % start_of_day)
    from_time = request.args.get('from', default = start_of_day, type = str)
    print("from_time = %s" % from_time)
    to_time = request.args.get('to', default = currenttime, type = str)
    print("to_time = %s" % to_time)
    filter_type = request.args.get('filter', default = '*', type = str)
    print("filter_type = %s" % filter_type)
    db_name = "weight_testing_db"
    print("db_name = %s" % db_name)
    return GETweight(from_time,to_time,filter_type,db_name)
    #return "Hello from GET/weight!"