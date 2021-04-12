# ------- 3rd party imports -------
from flask import Blueprint
from app.server.db.models import *
from app.server.db.helper import helper
from sqlalchemy import inspect

# ------- local imports -------
health_blueprint = Blueprint('health_blueprint', __name__)


@health_blueprint.route("/health")
def health():
    health_check = helper.health_check(HealthCheck)
    if health_check:
        return 'OK', 200

    return 'Internal server error', 500
