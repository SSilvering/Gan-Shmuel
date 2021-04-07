from weight_app import weight_app

@weight_app.route('/')
def index():
    return "Hello, World!"