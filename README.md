# Scripts and configs for the HGCROC

## Setup

```
ssh ldmx@ldmxdaq-test.cern.ch
cd pflib
srogue
```

Setup the DPM (0 or 1)
```
source dpm0_setup.sh
# or
source dpm1_setup.sh
```

## Running the tool

The script `runPF.py` will build a list of commands and then run `pflib`.

To see all the options:
```
python runPF.py -h
```

**NOTE: VERY IMPORTANT**
If the argument `--run` is not included, then the script will only print out the commands and not execute them.

- To configure with a general config file, e.g. `configs/march29_1400_LowBiasLEDFlash_Vref200.yaml` and ROCS 0 and 2:
```
python scripts/runPF.py --fconfig configs/march29_1400_LowBiasLEDFlash_Vref200.yaml --rocs 0 2 general
```

- To configure charge injection and daq (100 events):
```
python scripts/runPF.py charge 
```

- To configure bias (for all connectors add `--hdmi -2`):
```
python scripts/runPF.py --sipm 3784 --hdmi -2 bias
```

- To configure LED pulse:
```
python scripts/runPF.py --led 1500 led
```

- To do a phase scan:
```
python scripts/runPF.py pscan
```

- To do a phase and L1A offset scan:
```
python scripts/runPF.py sscan
```

- To get pedestal data
```
python scripts/runPF.py --tag bias3784_vref325roc0_ --odir data/march29 --nevents 10000 pedestal
```

- To change vref
```
python HGCROCSketches/scripts/runPF.py --value 325 --roc 0 vref
```

- To change l1offset
```
python HGCROCSketches/scripts/runPF.py --value 8 --roc 0 l1offset
```