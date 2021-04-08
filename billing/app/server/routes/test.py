# ------- 3rd party imports -------
from flask import Blueprint
from app.server.db.models import *
from app.server.db.helper import helper
# ------- local imports -------
test_blueprint = Blueprint('test_blueprint', __name__)

SQL_TEST_URI='sqlite:///temp.sql'

@test_blueprint.route("/test")
def test():
    helper.add_instance(Provider, name="provider1")
    helper.add_instance(Provider, name="provider2")
    helper.add_instance(Rate, product_name="potatoes", rate=350, scope='ALL')
    helper.add_instance(Rate, product_name="cucumbers", rate=290, scope='ALL')
    provider1_id = helper.get_provider_id("provider1")
    return provider1_id
