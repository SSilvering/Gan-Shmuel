import subprocess


def subprocess_cmd(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print(proc_stdout)


subprocess_cmd(f'mkdir hello && cd hello && echo hello > file.txt')

#
