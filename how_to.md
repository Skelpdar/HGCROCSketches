ssh ldmx@ldmxdaq-test.cern.ch
LDMX-TB-DAQ
cd pflib
srogue
source dpm1_setup.sh
./pflib/pftool cob1-dpm1 -s run/general_setup.txt
./pflib/pftool cob1-dpm1 -s run/charge_injection_setup_on.txt
rm -r data/led/
mkdir data/led
./pflib/pftool cob1-dpm1 -s run/pulseScan.txt

./pflib/pfdecoder -r 0 -a ./data/led/0.raw | tee ./data/led/0.txt
./pflib/pfdecoder -r 0 -a ./data/led/1.raw | tee ./data/led/1.txt
./pflib/pfdecoder -r 0 -a ./data/led/2.raw | tee ./data/led/2.txt
./pflib/pfdecoder -r 0 -a ./data/led/3.raw | tee ./data/led/3.txt
./pflib/pfdecoder -r 0 -a ./data/led/4.raw | tee ./data/led/4.txt
./pflib/pfdecoder -r 0 -a ./data/led/5.raw | tee ./data/led/5.txt
./pflib/pfdecoder -r 0 -a ./data/led/6.raw | tee ./data/led/6.txt
./pflib/pfdecoder -r 0 -a ./data/led/7.raw | tee ./data/led/7.txt
./pflib/pfdecoder -r 0 -a ./data/led/8.raw | tee ./data/led/8.txt
./pflib/pfdecoder -r 0 -a ./data/led/9.raw | tee ./data/led/9.txt
./pflib/pfdecoder -r 0 -a ./data/led/10.raw | tee ./data/led/10.txt
./pflib/pfdecoder -r 0 -a ./data/led/11.raw | tee ./data/led/11.txt
./pflib/pfdecoder -r 0 -a ./data/led/12.raw | tee ./data/led/12.txt
./pflib/pfdecoder -r 0 -a ./data/led/13.raw | tee ./data/led/13.txt
./pflib/pfdecoder -r 0 -a ./data/led/14.raw | tee ./data/led/14.txt
ls

scp -r ldmx@ldmxdaq-test.cern.ch:/home/ldmx/pflib/data/led ./chargeScan2
python run.py
