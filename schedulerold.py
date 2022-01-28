import os, sys, subprocess, random, time


def removeFile(name):
    os.system(f'rm -f { name }')


def getAvailableNodes():
    return [node.decode('UTF-8')[1:-1] for node in subprocess.check_output(['sinfo', '--partition=all', '--states=idle', '--format="%n"']).split()[1:]]


if len(sys.argv) < 2:
    print(
f"""Requires at least one argument:
- name of a .txt file containing a list of tasks
- task surrounded by quotation marks""")

else:
    tasks = []
    for arg in sys.argv[1:]:
        if arg[-4:] == '.txt':
            prefix = ''
            for line in open(arg).readlines():
                line = line.strip()
                if len(line) == 0:
                    prefix = ''
                elif line[-1] == ':':
                    prefix = line[:-1]
                else:
                    tasks.append(f'{ prefix } { line }'.strip())
        else:
            tasks.append(arg)

    removeFile('outputs/*')

    for i, task in enumerate(tasks):
        nodes = getAvailableNodes()

        while len(nodes) == 0:
            nodes = getAvailableNodes()
            time.sleep(0.1)

        file = open('run.sh', 'w+')        
        file.write(
f"""#!/bin/bash
#SBATCH --output=outputs/out{ i }.log
#SBATCH --partition=all
#SBATCH --nodelist={ random.choice(nodes) }

{ task }
""")
        file.close()
        os.system(f'sbatch run.sh')
    removeFile('run.sh')
