# import subprocess
#
#
# # def subprocess_cmd(command):
# #     process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
# #     proc_stdout = process.communicate()[0].strip()
# #     print(proc_stdout)
# #
# #
# # subprocess_cmd('mkdir hello && cd hello && echo hello > file.txt')
#
#
# def up_container(branch):
#     bashCommands = [f'mkdir -p /home/ec2-user/tmp/build_{branch}',
#                     f'cd /home/ec2-user/tmp/build_{branch}',
#                     'git clone https://github.com/SSilvering/Gan-Shmuel.git',
#                     f'cd /home/ec2-user/tmp/build_{branch}/{branch}',
#                     f'git checkout {branch}',
#                     'docker-compose up --build --force-recreate']
#
#     command = ' && '.join(x for x in bashCommands)
#     print(command)
#     print("+++++++++++++++++++++++++++++++++++++++++++++++")
#
#
# up_container('billing')
# "mkdir -p /home/ec2-user/tmp/build_tomer && cd /home/ec2-user/tmp/build_tomer && git clone https://github.com/SSilvering/Gan-Shmuel.git && cd /home/ec2-user/tmp/build_tomer/tomer && git checkout tomer && docker-compose up --build --force-recreate"
"""
Just a test comment, nothing special.....
In case I don't see you, good afternoon, good evening and good night!
"""