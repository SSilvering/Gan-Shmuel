# ------- 3rd party imports -------
from flask import Blueprint, request
from app.server.db.models import *
from app.server.db.helper import helper

# ------- local imports -------
bill_blueprint = Blueprint('bill_blueprint', __name__)


@bill_blueprint.route("/bill")
def bill():
    return '', 200
