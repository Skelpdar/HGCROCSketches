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

Help:
```
python runPF.py -h
```

**NOTE: VERY IMPORTANT**
If the argument `--run` is not included, then the script will only print out the commands and not execute them.

- To configure with a general config file, e.g. `configs/march29_1400_LowBiasLEDFlash_Vref200.yaml` and ROCS 0 and 2:
```
python scripts/runPF.py -c general --fconfig configs/march29_1400_LowBiasLEDFlash_Vref200.yaml --rocs 0 2 
```

- To configure charge injection and daq (100 events):
```
python scripts/runPF.py -c charge 
```

- To configure bias:
```
python scripts/runPF.py -c bias --sipm 3784
```

- To configure LED pulse:
```
python scripts/runPF.py -c led --led 1500
```

- To do a phase scan:
```
python scripts/runPF.py -c pscan
```

- To do a phase and L1A offset scan:
```
python scripts/runPF.py -c sscan
```

