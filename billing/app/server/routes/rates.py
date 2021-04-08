# ------- 3rd party imports -------
from flask import Blueprint, request
from flask import Blueprint, request,jsonify
import openpyxl
import os
from pathlib import Path
from app.server.db.helper import helper
from app.server.db.models import *
# ------- local imports -------
rates_blueprint = Blueprint('rates_blueprint', __name__)


@rates_blueprint.route("/rates", methods=['GET', 'POST'])
def rates():
    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        print(os.getcwd())
        xlsx_file = Path(os.getcwd()+'/app/static/rates.xlsx')
        wb_obj = openpyxl.load_workbook(xlsx_file)
        sheet = wb_obj.active

        title = True
        for row in sheet.iter_rows():
            if title:   # first row is title we skip it
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

        print("hello from POST/rates")
        return 'OK', 200
