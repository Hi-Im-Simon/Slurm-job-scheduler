import os


for i in range(1, 5):
	os.system(f'sudo scontrol update nodename=node0{ i } state=resume')
