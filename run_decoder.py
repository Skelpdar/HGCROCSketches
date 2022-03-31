# 31-41: 64-80,4 ??
# : 84-100,4 ??
# 41-48: 18-36,4
# 49-77: 8,124,4
# 78-88: 80-90
# 89: 84 

import os
import glob

runs = list(range(78,98))
values = list(range(80,90,1))
run_by_offset = dict(zip(runs, values))

# print(run_by_offset)

umn_path = "/u1/ldmx/diskless/minnesotaDPM/home/ldmx/data/"
odir = "data/march30/l1scan_80to90/"
os.system(f'mkdir -p {odir}')
for half in range(0,2):
    for run,value in run_by_offset.items():
        files = glob.glob(umn_path+"/run000{:03d}*".format(run))
        for ifile in files:
            cmd = f'/home/ldmx/pflib/pflib_jm/pfdecoder -r {half} -a {ifile} | tee {odir}/{value}_{half}.txt'
            #print(cmd)
            os.system(cmd)

