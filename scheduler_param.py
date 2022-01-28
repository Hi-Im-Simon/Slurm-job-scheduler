import os, random
from common import getAvailableNodes


def sched_param(args, param):
    scriptpath = args["SHARED"]+"/batchscript"+str(os.getpid())+".sh"
    while(1):
        prog = input()
        if(prog.lower() == "stop" or prog.lower() == "exit" or prog.lower() == "x"):
            break
#=================MULTIPLE PROGRAMS====================================
        if (prog[:6]=="!batch"):
            prog = prog.split()
            if (len(prog) > 3):
                print("Too many arguments - !batch takes a single text file and parameter n")
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
            #paramter param divides the node list into two lists - nodes with index lesser than param and greater than param. One of the lists can be empty.
            #If prog[2] is outside of range of the initial node list - no nodes are chosen
            #If prog[2] is inside the range:
            #   if prog[2] is greater than or equal to param then n2 is picked
            #   if prog[1] is less than param then n1 is picked
            if (param > len(nodes)-1 or param < 0):
                if(prog[2]<len(nodes) and prog[2]>=0):
                    script.write("#SBATCH --nodelist="+str(random.choice(nodes))+'\n\n')
                else:
                    script.close()
                    os.remove(scriptpath)
                    continue
            else:
                n1 = nodes[:param]
                n2 = nodes[param:]
                if (prog[2]>=param and prog[2] < len(nodes)):
                    script.write("#SBATCH --nodelist="+str(random.choice(n2))+'\n\n')
                elif (prog[2]<param and prog[2] > 0):
                    script.write("#SBATCH --nodelist="+str(random.choice(n1))+'\n\n')
                else:
                    script.close()
                    os.remove(scriptpath)
                    continue
 
 
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
            if (len(prog) > 2):
                print("Too many arguments - scheduler takes a single job and parameter n")
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
 
            if (param > len(nodes)-1 or param < 0):
                if(prog[2]<len(nodes) and prog[2]>=0):
                    script.write("#SBATCH --nodelist="+str(random.choice(nodes))+'\n\n')
                else:
                    script.close()
                    os.remove(scriptpath)
                    continue
            else:
                n1 = nodes[:param]
                n2 = nodes[param:]
                if (prog[1]>=param and prog[1] < len(nodes)):
                    script.write("#SBATCH --nodelist="+str(random.choice(n2))+'\n\n')
                elif (prog[1]<param and prog[1] > 0):
                    script.write("#SBATCH --nodelist="+str(random.choice(n1))+'\n\n')
                else:
                    script.close()
                    os.remove(scriptpath)
                    continue
 
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
