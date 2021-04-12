from . import weight_app
from .db_module import DB_Module

def unknown_func():
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