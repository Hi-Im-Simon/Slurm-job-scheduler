import os, sys, time


def removeFile(name):
    os.system(f'rm -f { name }')



if len(sys.argv) < 2:
    print(
f"""Requires at least one argument:
- name of a .txt file containing a list of tasks
- task surrounded by quotation marks""")

else:
    jobs = []
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
                    jobs.append(f'{ prefix } { line }'.strip())
        else:
            jobs.append(arg)

    removeFile('outputs/*')

    for i, job in enumerate(jobs):
        file = open('run.sh', 'w+')

        file.write(
f"""#!/bin/bash
#SBATCH --output=outputs/out{ i }.log

{ job }
""")
        file.close()
        
        os.system(f'sbatch run.sh')
    removeFile('run.sh')
