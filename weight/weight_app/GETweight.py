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
    sql_string = "SELECT id,direction,bruto,neto,products_id FROM sessions WHERE date BETWEEN %s AND %s;" % (from_time,to_time)
    if filter_type=="in" or filter_type=="out":
        sql_string+=" AND direction='%s'"
    myresults = mydb.fetch_new_data(sql_string)
    for ind in range(0,len(myresults)):
        id = int(myresults[ind]["id"])
        bruto = float(myresults[ind]["bruto"])
        neto = float(myresults[ind]["neto"])
        product_name = str(myresults[ind]["product_name"])
        direction = str(myresults[ind]["direction"])
        containers_list_from_db_list = mydb.fetch_new_data("SELECT containers_id FROM containers_has_sessions WHERE sessions_id = %d" % id)
        containers = json.dumps(containers_list_from_db_list, indent = 2)
        session_list = session_list.append( session(id, direction, bruto, neto, product_name, containers) )
    return json.dumps(myresults, indent = 7)