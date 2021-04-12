import json

from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from app.server.db.extensions import db  # importing db=sqlalchny()
from app.server.db.helper import helper  # importing helper = DbHelper(db)
from app.server.db.models import *  # import tables

# ------- local imports -------
provider_blueprint = Blueprint('provider_blueprint', __name__)


def create_id(name):
    helper.add_instance(Provider, name=name)
    new_name = helper.get_one(Provider, name=name)
    return jsonify(id=new_name.id, name=new_name.name)


@provider_blueprint.route("/provider/<id>", methods=['PUT'])
def put_collection(id):
    new_name = (request.form and request.form["name"]) or (request.json and request.json.get("name"))
    if new_name is None:
        return 'Bad parameters, expected {"name":"<name>"} or "name=<name>\n"', 400
    found_id = helper.get_one(Provider, id=id)
    if found_id is None:
        return "the <id> sent isn't related to any existing entry on the server\n", 406

    if helper.get_one(Provider, name=new_name):
        return "new Provider name already Exists\n", 400
    found_id.name = new_name
    helper.commit_changes()
    return "", 200


# @provider_blueprint.route("/provider", methods=['POST'])
# def provider():
#     args = request.json
#     name = args.get("provider")
#     found_name = helper.get_one(Provider, name=name)
#     if found_name:
#         return "", 200
#     else:
#         return create_id(name), 200


@provider_blueprint.route("/provider", methods=['POST'])
def provider():
    try:
        name = json.loads(request.data)['name']

    except (TypeError, KeyError):
        return 'Bad parameters, expected {"name":"<name>"}\n', 400

    found_name = helper.get_one(Provider, name=name)

    if found_name:
        return "Provider already Exists\n", 400

    else:
        return create_id(name), 200
