from . import weight_app
from .db_module import DB_Module
from flask import jsonify
import json, csv

def POSTbatch_weight(filename):
    filepath = f'./weight_app/in/{filename}'
    query_list = []

    # data = []
    is_csv = False
    query = f"INSERT INTO containers (id,weight,unit) VALUES (%s,%s,%s)"

    with open(filepath,'r') as my_file: #case if it's JSON
        try:
            data = json.load(my_file)
            for line in data:

                _id = line['id']
                weight = line['weight']
                unit = line['unit']
                values = (_id, weight,unit)

                query_list.append(values)

        except:
            is_csv = True


    if is_csv: #case if it's CSV
        with open(filepath,'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for line in reader:

                _id = list(line.values())[0]
                weight = list(line.values())[1]
                unit = list(line.keys())[1]
                values = (_id, weight,unit)

                query_list.append(values)

    retrived = ''
    db = DB_Module ()
    db.insert_new_data(query,query_list)
    retrived = db.fetch_new_data('SELECT * FROM containers')

    return jsonify(retrived)