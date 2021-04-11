#!/bin/sh
#pip install -r requirments.txt
export FLASK_APP=weight.py
flask run --host="0.0.0.0" --port=8080