#!/user/bin/env python3

#for i in range(0,15):
#    print("roc")
#    print("poke_param")
#    print("top")
#    print("phase")
#    print(i)
#    print("quit")
#    print("daq")
#    print("charge")
#    print("1000")
#    print(f'./data/march23/charge_dac100_phase_{i}.raw')
#    print("quit")
#    print("\n")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():

#    dac="10"
#    directory="./led_0/"
#    prefix="dac_"+dac+"_"

    directoryDict={
                    #"./charge/":{"legend":"LED Bias: 2500 DAC","color":"black"},
                    #"./led_2500/":{"legend":"LED Bias: 2500 DAC","color":"black"},
                    #"./regularScan_v2/":{"legend":"LED Bias: 2500 DAC","color":"black"},
                    #"./dpm0/ledSuperScan/24_":{"legend":"LED Bias: 2500 DAC","color":"black"},
                    "./chargeScan2/":{"legend":"LED Bias: 2500 DAC","color":"black"},
                    
                    
                    }

    f, ax = plt.subplots(figsize=(25*(1/2.54), 13.875*(1/2.54)))

    for key in directoryDict:
        directory=key

        listOfFiles = [ 
                        directory+"0.txt",
                        directory+"1.txt",
                        directory+"2.txt",
                        directory+"3.txt",
                        directory+"4.txt",
                        directory+"5.txt",
                        directory+"6.txt",
                        directory+"7.txt",
                        directory+"8.txt",
                        directory+"9.txt",
                        directory+"10.txt",
                        directory+"11.txt",
                        directory+"12.txt",
                        directory+"13.txt",
                        directory+"14.txt",
                        ]

        theDict = {'x':[], 'x_error':[], 'y':[], 'y_error':[]}
        x=[]
        y=[]
                     
        for currentFile in listOfFiles:
            phase=(int(currentFile.split(".")[1].split("/")[2]))
            #print(phase)
            #phase = int(currentFile.split(".")[1].split("/")[3].split("_")[1])
            with open(currentFile) as f:
                data = f.readlines()
            sample1 = []
            sample2 = []
            sample3 = []
            sample4 = []
            sample5 = []
            sample6 = []
            sample7 = []
            sample8 = []
            
            for line in data:
                if line[:3] == "  0":
                    currentData = line.split()
                    sample1.append(int(currentData[1]))
                    sample2.append(int(currentData[2]))
                    sample3.append(int(currentData[3]))
                    sample4.append(int(currentData[4]))
                    sample5.append(int(currentData[5]))
                    sample6.append(int(currentData[6]))
                    sample7.append(int(currentData[7]))
                    sample8.append(int(currentData[8]))
                    
#                    y.append(int(currentData[1]))
#                    x.append(0+(phase*(25/16)))
#                    y.append(int(currentData[2]))
#                    x.append(25+(phase*(25/16)))
#                    y.append(int(currentData[3]))
#                    x.append(50+(phase*(25/16)))
#                    y.append(int(currentData[4]))
#                    x.append(75+(phase*(25/16)))
#                    y.append(int(currentData[5]))
#                    x.append(100+(phase*(25/16)))
#                    y.append(int(currentData[6]))
#                    x.append(125+(phase*(25/16)))
#                    y.append(int(currentData[7]))
#                    x.append(150+(phase*(25/16)))
#                    y.append(int(currentData[8]))
#                    x.append(175+(phase*(25/16)))

            theDict["y"].append(float(np.mean(sample1)))
            theDict["y"].append(float(np.mean(sample2)))
            theDict["y"].append(float(np.mean(sample3)))
            theDict["y"].append(float(np.mean(sample4)))
            theDict["y"].append(float(np.mean(sample5)))
            theDict["y"].append(float(np.mean(sample6)))
            theDict["y"].append(float(np.mean(sample7)))
            theDict["y"].append(float(np.mean(sample8)))

            theDict["y_error"].append(float(np.std(sample1)))
            theDict["y_error"].append(float(np.std(sample2)))
            theDict["y_error"].append(float(np.std(sample3)))
            theDict["y_error"].append(float(np.std(sample4)))
            theDict["y_error"].append(float(np.std(sample5)))
            theDict["y_error"].append(float(np.std(sample6)))
            theDict["y_error"].append(float(np.std(sample7)))
            theDict["y_error"].append(float(np.std(sample8)))

            theDict["x"].append(0+(phase*(25/16)))
            theDict["x"].append(25+(phase*(25/16)))
            theDict["x"].append(50+(phase*(25/16)))
            theDict["x"].append(75+(phase*(25/16)))
            theDict["x"].append(100+(phase*(25/16)))
            theDict["x"].append(125+(phase*(25/16)))
            theDict["x"].append(150+(phase*(25/16)))
            theDict["x"].append(175+(phase*(25/16)))
                
            theDict["x_error"].append((25/16)/2)
            theDict["x_error"].append((25/16)/2)
            theDict["x_error"].append((25/16)/2)
            theDict["x_error"].append((25/16)/2)
            theDict["x_error"].append((25/16)/2)
            theDict["x_error"].append((25/16)/2)
            theDict["x_error"].append((25/16)/2)
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
    
#    ax.errorbar(x, y,
#                linestyle='None',
#                marker="o",
#                color="black",
#                markersize=2,
#                linewidth=0.5,
#                label="Led = "+dac,
#               )
#        
#    plt.xlabel("Time [ns]")
#    plt.ylabel("ADC Count")
#    plt.title("LED Flash, CERN 2022-03-26")
#    plt.tight_layout()
#    
#    leg1 = ax.legend(borderpad=0.5, loc=1, ncol=2, frameon=True,facecolor="white",framealpha=1)
#    leg1._legend_box.align = "left"
#    leg1.set_title("SiPM Bias = 45V\n LED Bias = 8.9V")
#    
#    ax.grid(True)
#    
#    f.savefig("./ledFlash_2500_show.pdf")
    
if __name__ == "__main__":
    main()
