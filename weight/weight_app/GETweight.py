from time import gmtime, strftime
import mysql.connector
from flask import jsonify
class session:
    id = "K-0000"
    direction = "none"
    bruto = 0
    neto = 0
    produce = "product_name"
    #container = ""
    def __init__(self, id, direction, bruto, neto, product_name): #, container):
        self.id = id
        self.direction = direction
        self.bruto = bruto
        self.neto = neto
        self.product_name = product_name
        #self.container = container


def GETweight(from_time,to_time,filter_type):
    #time_format yyyymmddhhmmss
    mydb = mysql.connector.connect(host="db", user="root", password="123", database="weight_testing_db")
    #mydb = DB_Module()
    sql_string = "SELECT * FROM sessions WHERE date BETWEEN %s AND %s;" % (from_time,to_time)
    if filter_type=="in" or filter_type=="out":
        sql_string+=" AND direction='%s'"
    mycursor = mydb.cursor()
    mycursor.execute(sql_string)
    myresults = mycursor.fetchall()
    #myresults = mydb.fetch_new_data(sql_string)
    for result in myresults:
        #sessions (id, direction, f, date, bruto, neto, trucks_id, products_id)
        id = result[0]
        print(id)
        bruto = result[4]
        print(bruto)
        neto = result[5]
        print(neto)
        product_id = result[7]
        print(product_id)
        mycursor.execute("SELECT product_name FROM products WHERE id='%d';" % product_id)
        produce = mycursor.fetchone()
        #This returns an empty set!
        ##mycursor.execute("SELECT containers_id FROM containers_has_sessions WHERE sessions_id='%s';" % result)
        ##container = mycursor.fetchone()
    return jsonify(id=id,bruto=bruto,neto=neto,produce=produce)