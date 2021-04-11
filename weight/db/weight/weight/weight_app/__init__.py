from flask import Flask, redirect, request, session
import requests
import mysql.connector
from mysql.connector import Error
#from .db_module import DB_Module



weight_app = Flask(__name__)
#db1 = DB_Module ()
#conn = db1.getConnection()

from weight_app import routes, GETweight, POSTweight
