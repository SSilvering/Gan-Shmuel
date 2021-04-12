from . import weight_app
from .db_module import DB_Module
from weight_app import requests

#a tuple of the all the apis that will be used in the project 
def GEThealth():
    api_tuple = ("index","batch-weight","unknown","item","session","post","weight")
    for item in api_tuple:
        uri = f"http://localhost:8080/{item}"
        req = requests.get(uri)
        print(req.status_code)
        if req.status_code < 200 or req.status_code > 299:
            res = f"APP api-{item} Status is {req.status_code}"
            return res
    return f"APP status is {req.status_code}"