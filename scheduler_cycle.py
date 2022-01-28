import os
from common import getAvailableNodes


def sched_cycle(args):
    scriptpath = args["SHARED"]+"/batchscript"+str(os.getpid())+".sh"
    i=-1
    while(1):
        prog = input()
        if(prog.lower() == "stop" or prog.lower() == "exit" or prog.lower() == "x"):
            break
#=================MULTIPLE PROGRAMS====================================
        if (prog[:6]=="!batch"):
            prog = prog.split()
            if (len(prog) > 2):
                print("Too many arguments (!batch takes a single text file)!")
                continue
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
            i+=1 #the iterator will loop through all the nodes in a cycle
            i%=len(nodes)
            script.write("#SBATCH --nodelist="+str(nodes[i])+'\n\n')
            ts = open(prog[1],'r')
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
            i+=1
            i%=len(nodes)
            script.write("#SBATCH --nodelist="+str(nodes[i])+'\n\n')
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
