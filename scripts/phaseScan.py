#!/user/bin/env python3

# V5 LED BIAS 2500 channel 0
# V3 LED BIAS 2500 channel 0
# V4 LED BIAS 1800 channel 0

#./pflib/pfdecoder -r 0 -a ./data/led2/0.raw | tee ./data/led2/0.txt
#./pflib/pfdecoder -r 0 -a ./data/led2/1.raw | tee ./data/led2/1.txt
#./pflib/pfdecoder -r 0 -a ./data/led2/2.raw | tee ./data/led2/2.txt
#./pflib/pfdecoder -r 0 -a ./data/led2/3.raw | tee ./data/led2/3.txt
#./pflib/pfdecoder -r 0 -a ./data/led2/4.raw | tee ./data/led2/4.txt
#./pflib/pfdecoder -r 0 -a ./data/led2/5.raw | tee ./data/led2/5.txt
#./pflib/pfdecoder -r 0 -a ./data/led2/6.raw | tee ./data/led2/6.txt
#./pflib/pfdecoder -r 0 -a ./data/led2/7.raw | tee ./data/led2/7.txt
#./pflib/pfdecoder -r 0 -a ./data/led2/8.raw | tee ./data/led2/8.txt
#./pflib/pfdecoder -r 0 -a ./data/led2/9.raw | tee ./data/led2/9.txt
#./pflib/pfdecoder -r 0 -a ./data/led2/10.raw | tee ./data/led2/10.txt
#./pflib/pfdecoder -r 0 -a ./data/led2/11.raw | tee ./data/led2/11.txt
#./pflib/pfdecoder -r 0 -a ./data/led2/12.raw | tee ./data/led2/12.txt
#./pflib/pfdecoder -r 0 -a ./data/led2/13.raw | tee ./data/led2/13.txt
#./pflib/pfdecoder -r 0 -a ./data/led2/14.raw | tee ./data/led2/14.txt
#ls

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

NSAMPLES = 8

def main():

    directoryDict={
        # directory: {legend, color}
#        "./data/charge_dac50_1k/":{"legend":"Highrange DAC = 50","color":"black"},
#        "./data/charge_dac40_1k/":{"legend":"Highrange DAC = 40","color":"red"},
#        "./data/charge_dac30_1k/":{"legend":"Highrange DAC = 30","color":"green"},
#        "./data/charge_dac5_1k/":{"legend":"Highrange DAC = 5","color":"blue"},
#        "./data/charge_dac1_1k/":{"legend":"Highrange DAC = 1","color":"magenta"},
#        "./data/lowrange_dac1_1k/":{"legend":"Lowrange DAC = 1","color":"black"},
#        "./data/lowrange_dac5_1k/":{"legend":"Lowrange DAC = 5","color":"red"},
#        "./data/lowrange_dac50_1k/":{"legend":"Lowrange DAC = 50","color":"green"},
#        "./data/lowrange_dac250_1k/":{"legend":"Lowrange DAC = 250","color":"blue"},
#        "./data/lowrange_dac500_1k/":{"legend":"Lowrange DAC = 500","color":"magenta"},
#        "./data/lowrange_dac1000_1k/":{"legend":"Lowrange DAC = 1000","color":"grey"},
#        "./data/led_dpm1_pscan/":{"legend":"LED = 1750 DAC","color":"black"},#LED

#        "./data/dpm1_charge/":{"legend":"LED = 1750 DAC","color":"red"}, #CHARGE
#        "./data/dpm1_charge2/":{"legend":"LED = 1750 DAC","color":"red"}, #CHARGE
#        "./data/dpm1_charge3/":{"legend":"LED = 1750 DAC","color":"red"}, #CHARGE
#        "./data/dpm1_charge4/":{"legend":"LED = 1750 DAC","color":"blue"},
#        "./data/dpm0_charge5/":{"legend":"Charge Injection","color":"black"},

#        "./data/dpm0_led1/":{"legend":"LED 1","color":"red"},
#        "./data/dpm0_led2/":{"legend":"LED 2","color":"green"},
#        "./data/charge4/":{"legend":"charge","color":"black"},
#        "./data/led4/":{"legend":"led","color":"red"},

#        "./data/ch0_LED2500/charge/":{"legend":"charge","color":"black"},
#        "./data/ch0_LED2500/led/":{"legend":"led","color":"red"},
#        "./data/ch4_LED2500/charge/":{"legend":"charge","color":"black"},
#        "./data/ch4_LED2500/led/":{"legend":"led","color":"red"},
#        "./data/dpm1_ch0_LED2500/charge/":{"legend":"charge","color":"black"},
#        "./data/dpm1_ch0_LED2500/led/":{"legend":"led","color":"red"},
#        "./data/dpm1_ch0_LED1700/charge/":{"legend":"charge","color":"black"},
#        "./data/dpm1_ch0_LED1700/led/":{"legend":"led","color":"red"},
#        "./data/dpm1_ch0_dacb0_SiPM_3784_LED_1000/charge/":{"legend":"charge","color":"black"},
#        "./data/dpm1_ch0_dacb0_SiPM_3784_LED_1000/led/":{"legend":"led","color":"red"},
        "../data/phaseScan/scan_PHASE_20220405_154131.csv"
    }

    f, ax = plt.subplots(figsize=(25*(1/2.54), 13.875*(1/2.54)))

    for key in directoryDict:
        directory=key
        listOfFiles = [directory+f"{i}.txt" for i in range(15)]

        theDict = {'x':[], 'x_error':[], 'y':[], 'y_error':[]}
        x=[]
        y=[]
                     
        for currentFile in listOfFiles:
            phase=(currentFile.split("data")[1].split("/")[2].split(".")[0])
            print(phase)
            phase=int(phase)
            
            with open(currentFile) as f:
                data = f.readlines()

            samples = {}
            for i in range(NSAMPLES):
                samples[i] = []
            
            for line in data:
                if line[:3] == "  0":
                    currentData = line.split()
                    for	i in range(NSAMPLES):
                        samples[i].append(int(currentData[i+1]))

            for i in range(NSAMPLES):
                theDict["y"].append(float(np.mean(samples[i])))
                theDict["y_error"].append(float(np.std(samples[i])))
                theDict["x"].append(i*25+(phase*(25/16)))
                theDict["x_error"].append((25/16)/2)

        df = pd.DataFrame(theDict)
        df = df.sort_values(by=['x'])

        ax.errorbar(df["x"], df["y"], yerr=df["y_error"], xerr=df["x_error"],
                    linestyle='None',
                    marker="o",
                    color=directoryDict[key]['color'],
                    markersize=2,
                    linewidth=0.5,
                    label=f"{directoryDict[key]['legend']}",
                   )
    
    plt.xlabel("Time [ns]")
    plt.ylabel("ADC Count")
    #plt.title("LED Flash, CERN 2022-03-26")
    plt.tight_layout()
    
    leg1 = ax.legend(borderpad=0.5, loc=1, ncol=1, frameon=True,facecolor="white",framealpha=1)
    leg1._legend_box.align = "left"
    leg1.set_title("SiPM Bias = 43.5 V\nLED Bias = 1700 DAC")
    
    ax.grid(True)
    
    plt.savefig("./scan_PHASE_20220405_154131.pdf")

if __name__ == "__main__":
    main()
