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

## Creating a .txt file with a task list
There are a few things to make your life easier and avoid unnecessary code.

The ways to fill the file:
- simply provide tasks line by line:

![image](https://user-images.githubusercontent.com/75808585/150392859-d7767712-f55d-4332-9ea8-dbf032c382b8.png)
- use a prefix methode to send multiple tasks using the same prefix (spaces are not required):

![image](https://user-images.githubusercontent.com/75808585/150393351-cf5a934b-d883-421c-b9be-c63df1f15bd3.png)
