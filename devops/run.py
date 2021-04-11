#!venv/bin/python3
import os
from flask import Flask, request, json, Response
import subprocess
# import logging

# logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

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
        
        
        branch = ''
        if data.get("ref"):

            branch = data.get("ref").split("/")[2]

            if branch in branches:
                if up_container(branch):
                    return Response(status=200)

        elif data.get("action") == "opened":
            branch = data.get("pull_request", {}).get("head", {}).get("billing")
            if data.get("head", {}).get("ref"):
                print("HI ** 38")
                branch = data.get("head", {}).get("ref")
                ## TODO: run tests on code, if it pass, approve PR and push to master
                print(branch)

    return Response(status=500, headers={"error":branch})


@app.route('/health', methods=['GET'])
def health():
    print("Health Check")
    return Response(status=200)


def up_container(branch):

    commands = f"chroot /host  /home/ec2-user/Gan-Shmuel/devops/scripts/up-container {branch}"

    try:
        p = subprocess.Popen(commands, stdout=subprocess.PIPE, shell=True)
        p_status = p.wait()
        (output, err) = p.communicate()
        
        print("Command output : ", output)
        print("Command exit status/return code : ", p_status)

    except Exception() as e:
        print("catch exception type: ", type(e))

        return False
    return True

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.getenv('PORT'), debug=os.getenv('DEBUG'))
