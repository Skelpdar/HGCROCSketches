# Scripts and configs for the HGCROC

## Running the tool

The script `runPF.py` will build a list of commands and then run `pflib`.

Help:
```
python runPF.py -h
 -c {general,charge,nocharge,pedestal,led,pscan,sscan} [{general,charge,nocharge,pedestal,led,pscan,sscan} ...], --commands {general,charge,nocharge,pedestal,led,pscan,sscan} [{general,charge,nocharge,pedestal,led,pscan,sscan} ...]
                        Commands to run separated by spaces
  -o ODIR, --odir ODIR  output directory that contains raw data e.g. ./data/led/
  --dpm DPM             DPM
  --board BOARD, -b BOARD
                        Board ID
  --rocs ROCS [ROCS ...]
                        ROCs (separated by spaces)
  --hdmi HDMI           HDMI connector
  --sipm SIPM           SiPM Bias
  --led LED             LED Bias
  --offset OFFSET       L1A offset
  --fconfig FCONFIG     Board ID
  --run                 Run
```

If the argument `--run` is not included, then the script will only print out the commands and not execute them.

- To configure with a general config file, e.g. `configs/march29_1400_LowBiasLEDFlash_Vref200.yaml` and ROCS 0 and 2:
```
python scripts/runPF.py -c general --fconfig configs/march29_1400_LowBiasLEDFlash_Vref200.yaml --rocs 0 2 --run
```

- To configure charge injection and daq (100 events):
```
python scripts/runPF.py -c charge --run
```

- To configure bias:
```
python scripts/runPF.py --sipm 3784
```

- To configure LED pulse:
```
python scripts/runPF.py --led 1500
```
