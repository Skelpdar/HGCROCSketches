#!/user/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():

    directoryDict={
        # directory: {legend, color}
        "./chargeScan2/":{"legend":"LED Bias: 2500 DAC","color":"black"},
    }

    f, ax = plt.subplots(figsize=(25*(1/2.54), 13.875*(1/2.54)))

    for key in directoryDict:
        directory=key
        listOfFiles = [directory+f"{i}.txt" for i in range(15)]

        theDict = {'x':[], 'x_error':[], 'y':[], 'y_error':[]}
        x=[]
        y=[]
                     
        for currentFile in listOfFiles:
            phase=(int(currentFile.split(".")[1].split("/")[2]))
            
            with open(currentFile) as f:
                data = f.readlines()

            samples = {}
            for i in range(8):
                samples[i] = []
            
            for line in data:
                if line[:3] == "  0":
                    currentData = line.split()
                    for	i in range(8):
                        samples[i].append(int(currentData[i+1]))

            for i in range(8):
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
    leg1.set_title("SiPM Bias = 43.5 V")
    
    ax.grid(True)
    
    plt.savefig("./chargeScan.pdf")

if __name__ == "__main__":
    main()
