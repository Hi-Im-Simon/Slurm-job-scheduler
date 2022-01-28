import subprocess


def getAvailableNodes(partition_name):
    return [node.decode('UTF-8')[1:-1] for node in subprocess.check_output(['sinfo', f'--partition={ partition_name }', '--states=idle', '--format="%n"']).split()[1:]]