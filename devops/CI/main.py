#!venv/bin/python3

from flask import Flask, request, json

app = Flask(__name__)


@app.route('/')
def home():
    return 'test home'


@app.route('/github', methods=['POST'])
def github():
    if request.headers['Content-Type'] == 'application/json':
        my_info = json.dumps(request.json)
        print(my_info)
        return my_info


@app.route('/health', methods=['GET'])
def health():
    return 'Hi'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
