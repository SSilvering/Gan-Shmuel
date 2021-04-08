#!venv/bin/python3
import os
from flask import Flask, request, json, Response
import subprocess


branches = ['billing', 'weight', 'devops']
app = Flask(__name__)


@app.route('/')
def home():
    return Response(status=403)


@app.route('/webhook', methods=['POST'])
def hook():

    if request.headers['Content-Type'] == 'application/json':
        data = request.get_json()
        
        if data.get("repository", {}).get("name") != "Gan-Shmuel":
            return "Ignore commit. Repository diffrent."
        
        branch = data.get("ref").split("/")[2]

        if branch in branches:
            if up_container(branch):
                return Response(status=200)
        
    return Response(status=500)


@app.route('/health', methods=['GET'])
def health():
    print("Health Check")
    return Response(status=200)


def up_container(branch):
    bashCommands = [ "chroot /host",
                    f'mkdir -p /home/ec2-user/tmp/build_{branch}',
                    f'cd /home/ec2-user/tmp/build_{branch}',
                    'git clone https://github.com/SSilvering/Gan-Shmuel.git',
                    f'cd /home/ec2-user/tmp/build_{branch}/Gan-Shmuel/{branch}',
                    f'git checkout {branch}',
                    'docker-compose up --build --force-recreate']


    command = ' && '.join(x for x in bashCommands)

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        proc_stdout = process.communicate()[0].strip()
        print(proc_stdout)
        print('Command executed successfully')

    except Exception() as e:
        print(type(e))
        return False
    return True

###
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.getenv('PORT'))
    # app.run(host="0.0.0.0", port=80, debug=True)
