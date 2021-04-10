# ------- 3rd party imports -------
from flask import Blueprint, request
from flask import Blueprint, request, jsonify
import openpyxl
import os
from pathlib import Path
from app.server.db.helper import helper
from app.server.db.models import *

# ------- local imports -------
rates_blueprint = Blueprint('rates_blueprint', __name__)


@rates_blueprint.route("/rates", methods=['GET'])
def download_rates_to_xml():
    return "OK\n", 200


@rates_blueprint.route("/rates", methods=['POST'])
def upload_xml_data():
    data = (request.form and request.form["file"]) or (request.json and request.json.get("file"))

    if data is None or not os.path.isfile('/in/'+data):
        return 'Bad parameters, expected {"file":"<name>"} or "file=<name>"\n', 400
    xlsx_file = Path('/in/' + data)
    try:
        wb_obj = openpyxl.load_workbook(xlsx_file)
    except:
        return f'Bad file {data}, unreadable or wrong format\n', 500
    sheet = wb_obj.active

    title = True
    for row in sheet.iter_rows():
        if title:  # first row is title we skip it
            title = False
            continue

        record = helper.get_one(Rate, product_name=row[0].value)
        if record is not None:
            print(f'value {row[0].value} already exists, updating...')
            record.rate = row[1].value
            record.scope = row[2].value
            helper.commit_changes()
        else:
            helper.add_instance(Rate, product_name=row[0].value,
                                rate=row[1].value,
                                scope=row[2].value)

    return 'OK\n', 200
