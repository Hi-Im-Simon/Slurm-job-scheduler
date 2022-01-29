import sys

from scheduler_random import sched_random
from scheduler_cycle import sched_cycle
from scheduler_param import sched_param


# def userInput():
 
 
if len(sys.argv) < 3:
    print(
f"""You need to provide 2 additional arguments:
- path to the configuration file
- name of the algorithm you want to use for scheduling (random, cycle, param)"""
)
else:
    conf = open(sys.argv[1])
    args = dict()
    
    for line in conf.readlines():   #reading through the .conf file and adding parameters to a dictionary
        line = line.split('=')
        line = [line[i].strip() for i in range(len(line))]
        args[line[0]] = line[1]
    
    if(args["SHARED"][-1] == '/'):
        args["SHARED"] = args["SHARED"][:len(args["SHARED"])-1]
    
    if(sys.argv[2] == "random"):
        sched_random(args)
    elif(sys.argv[2] == "cycle"):
        sched_cycle(args)
    elif(sys.argv[2] == "param"):
        if (len(sys.argv) < 4):
            print("Error: Parametric scheduling requires third argument - threshold")   #taking a third initial argument - threshold
        else:
            sched_param(args, sys.argv[3])
