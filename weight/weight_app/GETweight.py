from time import gmtime, strftime
import mysql.connector

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


def GETweight(from_time,to_time,filter_type,db_name):
    #time_format yyyymmddhhmmss
    mydb = mysql.connector.connect(host="db", user="root", password="123", database=db_name)
    sql_string = "SELECT id FROM sessions WHERE date BETWEEN %d AND %d;" % (from_time,to_time)
    if filter_type=="in" or filter_type=="out":
        sql_string+=" AND direction='%s'"
    mycursor = mydb.cursor()
    mycursor.execute(sql_string)
    myresults = mycursor.fetchall()
    session_list =[]
    for result in myresults:
        id = result
        print("id = %s" % id)
        mycursor.execute("SELECT bruto FROM sessions WHERE id='%d';" % result)
        bruto = mycursor.fetchone()
        print("bruto = %s" % bruto)
        mycursor.execute("SELECT neto FROM sessions WHERE id='%d';" % result)
        neto = mycursor.fetchone()
        print("neto = %s" % neto)
        mycursor.execute("SELECT products_id FROM sessions WHERE id='%d';" % result)
        product_id = mycursor.fetchone()
        print("product_id = %s" % product_id)
        mycursor.execute("SELECT product_name FROM products WHERE id='%d';" % product_id)
        produce = mycursor.fetchone()
        print("produce = %s" % produce)
        #This returns an empty set!
        ##mycursor.execute("SELECT containers_id FROM containers_has_sessions WHERE sessions_id='%s';" % result)
        ##container = mycursor.fetchone()
        session_list.append( session(id, filter_type, bruto, neto, produce) )#, container) )

    return "{ \"id\": <id>, \"direction\": in/out/none, \"bruto\": <int>, //in kg \"neto\": <int> or \"na\", \"produce\": <str> }"#, \"container\": <str> }"