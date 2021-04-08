
from weight_app import weight_app, requests
from time import gmtime, strftime
from flask import request
import mysql.connector

class session:
    id = "K-0000"
    direction = "none"
    bruto = 0
    neto = 0
    produce = "product_name"
    container = ""
    def __init__(self, id, direction, bruto, neto, product_name, container): 
        self.id = id
        self.direction = direction
        self.bruto = bruto
        self.neto = neto
        self.product_name = product_name
        self.container = container


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
def GETweight():
    #time_format yyyymmddhhmmss
    currenttime = strftime("%Y%m%d%H%M%S", gmtime())
    start_of_day = strftime("%Y%m%d000000", gmtime())
    from_time = request.args.get('from', default = start_of_day, type = str)
    to_time = request.args.get('to', default = currenttime, type = str)
    filter_type = request.args.get('filter', default = '*', type = str)
    db_name = "my_sql_weight"
    mydb = mysql.connector.connect(
        host="db",
        user="root",
        password="123",
        database=db_name
    )
    session_list =[]
    sql_string = "SELECT id FROM sessions WHERE date BETWEEN %d AND %d" % (from_time,to_time)
    if filter_type=="in" or filter_type=="out":
        sql_string+=" AND direction='%s'"
    mycursor = mydb.cursor()
    mycursor.execute(sql_string)
    myresults = mycursor.fetchall()
    for result in myresults:
        id = result
        mycursor.execute("SELECT bruto FROM sessions WHERE id='%d'" % result)
        bruto = mycursor.fetchone()
        mycursor.execute("SELECT neto FROM sessions WHERE id='%d'" % result)
        neto = mycursor.fetchone()
        mycursor.execute("SELECT products_id FROM sessions WHERE id='%d'" % result)
        product_id = mycursor.fetchone()
        mycursor.execute("SELECT product_name FROM products WHERE id='%d'" % product_id)
        produce = mycursor.fetchone()
        mycursor.execute("SELECT containers_id FROM containers_has_sessions WHERE sessions_id='%s'" % result)
        container = mycursor.fetchone()
        session_list.append( session(id, filter_type, bruto, neto, produce, container) )

    return "{ \"id\": <id>, \"direction\": in/out/none, \"bruto\": <int>, //in kg \"neto\": <int> or \"na\", \"produce\": <str>, \"container\": <str> }"
#def GETweight_startup():
    #return "Hello from GET/weight!"