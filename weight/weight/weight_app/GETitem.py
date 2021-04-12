from . import weight_app
from .db_module import DB_Module
from datetime import datetime
from flask import jsonify

def GETitem(item_id,from_time,to_time):
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