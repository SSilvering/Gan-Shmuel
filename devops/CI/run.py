#!venv/bin/python3
import os
from flask import Flask, request, json, jsonify, Response
import subprocess


branches = ['billing', 'weight', 'devops']
branch = ''
app = Flask(__name__)


@app.route('/')
def home():
    return Response(status=403)


@app.route('/webhook', methods=['POST'])
def hook():
    if request.headers['Content-Type'] == 'application/json':
        data = json.dumps(request.json)
        print(data)

        if check_push(data):
            if up_container(branch):
                return Response(status=200)
        
        return Response(status=500)


@app.route('/health', methods=['GET'])
def health():
    print("Health Check")
    return Response(status=200)


def check_push(data):
    global branch
    branch = data['ref'].split('/')[2]
    if branch in branches:
        return True
    else:
        return False


def up_container(branch):
    #'chroot /host'
    bashCommands = [ 
                    f'cd /home/ec2-user/Gan-Shmuel/{branch}', 
                    f'git checkout {branch}',
                    'git pull --rebase', 
                    'docker-compose up --build --force-recreate']

    for command in bashCommands:
        try:
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            print('test OK_1')
        except Exception() as e:
            print(error)
            return False
    return True
    


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.getenv('PORT'))
