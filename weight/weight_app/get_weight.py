from time import gmtime, strftime
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

def get_weight(from_time,to_time,filter_type,db_name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123",
        database="db_name"
    )
    mycursor = mydb.cursor()
    session_list =[]
    sql_string = "SELECT id FROM sessions WHERE date BETWEEN %d AND %d" % (from_time,to_time)
    if filter_type=="in" or filter_type=="out":
        sql_string+=" AND direction='%s'"
    mycursor.execute(sql_string)
    myresults = mycursor.fetchall()
    #is it possible? myresults = mycursor.execute(sql_string).fetchall()
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