from flask import Flask, redirect, request, session
import requests

weight_app = Flask(__name__)

from weight_app import routes