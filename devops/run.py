#!venv/bin/python3
import os
from flask import Flask, request, json, Response
import subprocess
# import logging

# logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

branches = ['billing', 'weight']
ports = {'weight_prod': '8084', 'weight_stg': '8083', 'billing_prod': '8082', 'billing_stg': '8081', 'test_port': '8085'}
flags = {'commit': 'commit', 'push': 'push'}
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
        if data.get("ref"):          ## STAGING (if Master -> Run Testing)

            branch = data.get("ref").split("/")[2]
            sha = data.get("after")

            if branch == 'master':
                temp_ports = ports.get('billing_prod') + ';' + ports.get('weight_prod') + ';' # Sent 2 ports
                if up_container(branch, sha, port=temp_ports, flag=flags.get('commit')):
                    return Response(status=200)
            else:
                
                if branch in branches:
                    if up_container(branch, sha, port=ports.get(branch+'_stg'), flag=flags.get('commit')):
                        return Response(status=200)

    return Response(status=400)


@app.route('/health', methods=['GET'])
def health():
    print("Health Check")
    return Response(status=200)

def up_container(branch, sha, port, flag):

    commands = f"chroot /host  /home/ec2-user/Gan-Shmuel/devops/scripts/up-container {branch} {sha} {port} {flag} > script.out"

    p = subprocess.Popen(commands, stdout=subprocess.PIPE, shell=True)

    try:        
        (output, err) = p.communicate()
        p_status = p.wait()
        
        print("Command output : ", output)
        print("Command exit status/return code : ", p_status)

    except Exception() as e:
        print("catch exception type: ", type(e))

        return False
    return True

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.getenv('PORT'), debug=os.getenv('DEBUG'))
