from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from app.server.db.extensions import db #importing db=sqlalchny()
from app.server.db.helper import helper #importing helper = DbHelper(db)
from app.server.db.models import *      #import tables

# ------- local imports -------
provider_blueprint = Blueprint('provider_blueprint', __name__)

def create_id(name):
    helper.add_instance(Provider, name=name)
    new_name = helper.get_one(Provider, name=name)
    return jsonify(id=new_name.id,name=new_name.name)

@provider_blueprint.route("/provider/<id>", methods=['PUT'])
def put_collection(id):
    args = request.json
    new_name = args.get("new_name")
    found_id = helper.get_one(Provider, id=id)
    found_id.name = new_name
    helper.commit_changes()
    return "", 200
#curl -i -X PUT -H 'Content-Type: application/json' -d '{"new_name": "test---------<<"}' http://127.0.0.1:5000/provider/10

@provider_blueprint.route("/provider", methods=['POST'])
def provider():    
    args = request.json                     #get arg from post
    name = args.get("provider")             #get provider name from args
    found_name = helper.get_one(Provider, name=name)
    if found_name: # if True
        # print("name: ",name, "allready excit in id:", found_name.id)
        return "", 200
    else:   #name not in Provider table
        return  create_id(name) ,200
    return "", 200
# curl -i -X POST -H 'Content-Type: application/json' -d '{"provider": "ProviderName"}' http://127.0.0.1:5000/provider