
from weight_app import weight_app, requests



@weight_app.route('/')
@weight_app.route('/index')
def index():
    return "Hello, World!"


@weight_app.route('/health', methods=['GET', 'POST'])
def health_check(api='<item>'):
    #a tuple of the all the apis that will be used in the project 
    api_tuple = ("index","batch-weight","unknown","item","session","post","weight")
    for item in api_tuple:
        uri = f"http://localhost:5000/{item}"
        req = requests.get(uri)
        print(req.status_code)
        if req.status_code < 200 or req.status_code > 299:
            res = f"APP Status is {req.status_code}"
            return res
    return f"APP status is {req.status_code}"
    
