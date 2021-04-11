#!venv/bin/python3
import os
from flask import Flask, request, json, Response
import subprocess
# import logging

# logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

branches = ['billing', 'weight', 'master']
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
            commit = data.get("after")

            if branch in branches:
                if up_container(branch, commit):
                    return Response(status=200)

        elif data.get("action") == "opened":
            branch = data.get("pull_request", {}).get("head", {}).get("ref")
            commit = data.get("pull_request", {}).get("head", {}).get("sha")

            if branch in branches:                
                ## TODO: run tests on code, if it pass, approve PR and push to master
                if up_container(branch, commit):
                    return Response(status=200)

            ## docker exec /app/testing.sh and see whats returns, if return OK, shuting down container and power it up on production mode (port 8082 or 8084 fit to the branch).
            ## if it fails, return 1 to flask and annonce the commiter.
    return Response(status=500, headers={"error":branch})


## if billing push -> up container (staging)
## elif billing PR -> up container and run docker-compose exec app/test
## if  docker-compose exec app/test 0 -> turn down container
## 
## if pr approve and occurred merge to master -> up container on production port (billing 8082 and weight 8084)



@app.route('/health', methods=['GET'])
def health():
    print("Health Check")
    return Response(status=200)

def up_container(branch, commit):

    commands = f"chroot /host  /home/ec2-user/Gan-Shmuel/devops/scripts/up-container {branch} {commit} > script.out"

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
