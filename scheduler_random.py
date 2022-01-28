import os, random
from common import getAvailableNodes


def sched_random(args):
    scriptpath = f'{ args["SHARED"] }/batchscript{ str(os.getpid()) }.sh'   #creating a path and filename for the temporary sbatch file
    while(1):
        prog = input()
        if(prog.lower() == "stop" or prog.lower() == "exit" or prog.lower() == "x"):
            break
#=================MULTIPLE PROGRAMS====================================
        if (prog[:6]=="!batch"):    #checking if command !batch was used. If so, input should consist of 2 arguments - 
            prog = prog.split()     #!batch and a text file with a list of jobs
            if (len(prog) > 2):
                print("Too many arguments (!batch takes a single text file)!")
                continue
            nodes = getAvailableNodes(args['partition'])
            if (len(nodes) == 0):
                print("Error: No Aviable Nodes")
                exit()
            script = open(scriptpath,'w')
 
            script.write("#!/bin/bash\n")
 
            for key,value in args.items():  #writing SBATCH directives from dictionary to the temporary file
                if(key=="SHARED"):
                    continue
                script.write("#SBATCH --"+key+'='+value+'\n')
            script.write("#SBATCH --nodelist="+str(random.choice(nodes))+'\n\n') #picking a random node from a list
            ts = open(prog[1],'r') #writing all the tasks to the file
            for task in ts.readlines():
                if(task[-3:] == ".py"):
                    script.write("python3 "+task+'\n')
                else:
                    script.write(task+'\n')
            script.close()
            st = os.stat(scriptpath)
            os.chmod(scriptpath,st.st_mode | 0o111)
            os.system("sbatch "+scriptpath)
            os.remove(scriptpath)
#==================SINGLE PROGRAM======================================
        else:
            nodes = getAvailableNodes(args['partition'])
            if (len(nodes)==0):
                print("Error: No Aviable Nodes")
                exit()
            script = open(scriptpath,'w')
 
            script.write("#!/bin/bash\n")
 
            for key,value in args.items():
                if(key=="SHARED"):
                    continue
                script.write("#SBATCH --"+key+'='+value+'\n')
            nod = random.choice(nodes)
            print(nod)
            script.write("#SBATCH --nodelist="+str(nod)+'\n\n')
            if(prog[-3:] == ".py"):
                script.write("python3 "+prog+'\n')
            else:
                script.write(prog+'\n')
            script.close()
            st = os.stat(scriptpath)
            os.chmod(scriptpath,st.st_mode | 0o111)
            os.system("sbatch "+scriptpath)
            os.remove(scriptpath)
    return
