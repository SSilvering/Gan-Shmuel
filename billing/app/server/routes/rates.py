# ------- 3rd party imports -------
from flask import Blueprint, request

# ------- local imports -------
rates_blueprint = Blueprint('rates_blueprint', __name__)


@rates_blueprint.route("/rates", methods=['GET', 'POST'])
def rates():
    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        pass
