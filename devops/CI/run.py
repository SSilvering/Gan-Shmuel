#!venv/bin/python3
import os
from flask import Flask, request, json, Response
from git import Repo



branches = ['billing', 'weight', 'devops']

app = Flask(__name__)


@app.route('/')
def home():
    return 'test home'


@app.route('/webhook', methods=['POST'])
def hook():
    if request.headers['Content-Type'] == 'application/json':
        data = json.dumps(request.json)
        print(data)

        if check_push(data):
            # repo = Repo(current_app.config.get('REPO_PATH'))
            repo = Repo('https://github.com/SSilvering/Gan-Shmuel.git') ## CHANGE IT        
            origin = repo.remotes.origin
            origin.pull('--rebase')
            return Response(status=200)


@app.route('/health', methods=['GET'])
def health():
    print("Health Check")
    return Response(status=200)


def check_push(data):
    branch = data['ref'].split('/')[2]
    if branch in branches:
        return True
    else:
        return False


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.getenv('PORT'))
