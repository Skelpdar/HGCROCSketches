import os
import argparse

def main(args):

    inputDir = args.idir
    for link in args.links.split(','):
        if args.superScan:
            # loop over phase values and L1A offset
            offsetList=[1,8,16,24,32,48,56,64,72,80,88,96,104]
            for phase in range(0,15):
                for offset in offsetList:
                    fname = f'{inputDir}/{offset}_{phase}'
                    cmd = f'./pflib/pfdecoder -r {link} -a {fname}.raw | tee {fname}.txt'
                    print(cmd)
                    #os.system(cmd)
        if args.phaseScan:
            # loop over phase values:
            for phase in range(0,15):
                fname = f'{inputDir}/{offset}'
                cmd = f'./pflib/pfdecoder -r {link} -a {fname}.raw | tee {fname}.txt'
                print(cmd)

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--superScan','--ss',dest='superScan',action='store_true',help='decode super scan')
    parser.add_argument('--phaseScan','-p',dest='phaseScan',action='store_true',help='decode phase scan')
    parser.add_argument('-i',dest='idir',type=str,required=True,help='input dir that contains raw data e.g. ./data/led/')
    parser.add_argument('--links',type=str,required=True,help='links to decode - split by commas')

    main(args)
