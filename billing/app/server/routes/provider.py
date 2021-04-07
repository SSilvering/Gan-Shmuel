# ------- 3rd party imports -------
from flask import Blueprint

# ------- local imports -------
provider_blueprint = Blueprint('provider_blueprint', __name__)


@provider_blueprint.route("/provider")
def provider():
    pass
