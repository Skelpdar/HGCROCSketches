# 31-41: 64-80,4 ??
# 41-1: 84-100,4 ??
# 41-48: 18-36,4
# 49-100: 18

import os
import glob

runs = list(range(49,78))
values = list(range(8,124,4))
run_by_offset = dict(zip(runs, values))

# print(run_by_offset)

umn_path = "/u1/ldmx/diskless/minnesotaDPM/home/ldmx/data/"
odir = "data/march30/l1scan/"
os.system(f'mkdir -p {odir}')
for half in range(0,2):
    for run,value in run_by_offset.items():
        files = glob.glob(umn_path+"/run000{:03d}*".format(run))
        for ifile in files:
            cmd = f'/home/ldmx/pflib/pflib_jm/pfdecoder -r {half} -a {ifile} | tee {odir}/{value}_{half}.txt'
            #print(cmd)
            os.system(cmd)

