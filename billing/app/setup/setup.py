# ------- 3rd party imports -------
from flask import Flask
import pymysql

# ------- local imports -------
from app.server.routes.health import health_blueprint
from app.server.routes.bill import bill_blueprint
from app.server.routes.provider import provider_blueprint
from app.server.routes.rates import rates_blueprint
from app.server.routes.truck import truck_blueprint
from app.server.routes.test import test_blueprint
from app.server.routes.truckPut import truckPut_blueprint
from app.server.routes.truckGet import truckGet_blueprint

# ------- local imports -------
from app.server.db.extensions import db


def create_app(config_file):
    """
    Creating and returning the app
    """

    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    db.init_app(app)

    with app.app_context():
        db.create_all()
        app.register_blueprint(health_blueprint)
        app.register_blueprint(bill_blueprint)
        app.register_blueprint(provider_blueprint)
        app.register_blueprint(rates_blueprint)
        app.register_blueprint(truck_blueprint)
        app.register_blueprint(test_blueprint)
        app.register_blueprint(truckPut_blueprint)
        app.register_blueprint(truckGet_blueprint)
        return app
