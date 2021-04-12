from flask import Flask, redirect, request, session
import requests
import mysql.connector
from mysql.connector import Error

weight_app = Flask(__name__)

from weight_app import routes, GETweight, POSTweight, GETunknown, GETitem, GEThealth, GETsession, POSTbatch_weight
