import sys
import subprocess
import time

procs = []
starttime = time.time()
for i in range(4):
    proc = subprocess.Popen([sys.executable, 'main.py', '-s', '/home/ec2-user/SST_ETBD_09_04_22/SST-ETBD_Code/inputs/Test'+str(i)])
    procs.append(proc)

for proc in procs:
    proc.wait()
endtime = time.time()
print("whole program runtime = {} seconds".format(endtime - starttime))    