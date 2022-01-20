# Slurm-job-scheduler

## Job scheduler
- `scheduler.py` can be executed with any amount of arguments passed (arguments can be `.txt files` or/and `whole tasks in quotation marks`)
- an example of execution can be `python3 scheduler.py "python3 tasks/task1.py" tasks/tasks.txt "hostname"`, which will send:
    * 2 tasks from quotation marks (`"python3 tasks/task1.py"` and `"hostname"`)
    * any amount of tasks located in `tasks/tasks.txt` file

## Node resumer
- `resume-nodes.py` can be executed to resume all nodes in cluser, but has to be customized according to cluster configuration
- command will return warnings in case one or more nodes are in _idle_ state
- `python3 resume-nodes.py` to execute
