from . import weight_app
from .db_module import DB_Module
from flask import jsonify

def GETsession(id):
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
                select_query = f"SELECT t1.id, t1.trucks_id, t1.bruto, t1.bruto-t1.neto AS 'truckTara', t1.neto FROM sessions t1, trucks t2 WHERE t1.id = {id} and t1.trucks_id = t2.truckid"
            else:
                select_query = f"SELECT t1.id, t1.trucks_id, t1.bruto FROM sessions t1, \
                    trucks t2 WHERE t1.id = {id} and t1.trucks_id = t2.truckid"
        data = db.fetch_new_data(select_query)
        session = []
        #for ind in range(0, len(data)):
        for res in data:
            session.append(res)
        return jsonify(session)

    return "provide a truck ID"