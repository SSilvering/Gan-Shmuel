from weight_app import weight_app, requests



@weight_app.route('/')
@weight_app.route('/index')
def index():
    return "Hello, World!"


@weight_app.route('/health')
def health_check():
    req = requests.get("http://localhost:5000/weight")
    print(req.status_code)
    r = req.status_code
    return str(r)
    
    
