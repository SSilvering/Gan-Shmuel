from . import weight_app
from .db_module import DB_Module
import json
from flask import jsonify
class session:
    id = "K-0000"
    direction = "none"
    bruto = 0
    neto = 0
    produce = "product_name"
    containers = []
    def __init__(self, id, direction, bruto, neto, product_name, containers):
        self.id = id
        self.direction = direction
        self.bruto = bruto
        self.neto = neto
        self.product_name = product_name
        self.containers = ["0","0"]

def GETweight(from_time,to_time,filter_type):
    #time_format yyyymmddhhmmss
    mydb = DB_Module()
    session_list = []
    sql_string = "SELECT id,direction,bruto,neto,products_id, containers FROM sessions WHERE date BETWEEN %s AND %s" % (from_time,to_time)
    if filter_type=="in" or filter_type=="out":
        sql_string+=" AND direction='%s'" % filter_type
    sql_string+=";"
    myresults = mydb.fetch_new_data(sql_string)
    for ind in range(0,len(myresults)):
        id = int(myresults[ind]["id"])
        bruto = float(myresults[ind]["bruto"])
        neto = float(myresults[ind]["neto"])
        products_id = int(myresults[ind]["products_id"])
        product_name_from_db = mydb.fetch_new_data("SELECT product_name FROM products WHERE id = %d" % products_id)
        product_name = json.dumps(product_name_from_db, indent = 2)
        direction = str(myresults[ind]["direction"])
        containers = str(myresults[ind]["containers"])
        session_list.append( session(id, direction, bruto, neto, product_name, containers) )
    return json.dumps(myresults, indent = 7)
