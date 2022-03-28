import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def read():

    phaseList=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    offsetList=[1,8,16,24,32,48,56,64,72,80,88,96,104]
    #phaseList=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    #offsetList=[24]

    theDict = {'x':[], 'x_error':[], 'y':[], 'y_error':[], "channel":[]}

    dfList = []

    for channel in range(0,37):
        channelString = "  "+str(channel) if channel < 10 else " "+str(channel)
        for offset in offsetList:
            for phase in phaseList:
                currentFile=f"./ledSuperScan_10_noLED/{offset}_{phase}.txt"
                #currentFile=f"./chargeSuperScan/{offset}_{phase}.txt"
                             
                with open(currentFile) as f:
                    data = f.readlines()
                    
                samples = {}
                for i in range(8):
		    samples[i] = []
                
                for line in data:
                    if line[:3] == channelString:
                        currentData = line.split()
                        for i in range(8):
                            samples[i].append(int(currentData[i+1]))

                for i in range(8):
                    theDict["channel"].append(int(channelString))
                    theDict["y"].append(float(np.mean(samples[i])))
                    theDict["y_error"].append(float(np.std(samples[i])))
                    theDict["x"].append(offset*25+i*25+(phase*(25/16)))
                    theDict["x_error"].append((25/16)/2)

    df = pd.DataFrame(theDict)
    df=df.sort_values(by=['x'])
    df.to_pickle("df.pickle")
  
def plot():
    f, ax = plt.subplots(figsize=(25*(1/2.54), 13.875*(1/2.54)))
    df = pd.read_pickle("df_original.pickle")
        
    for channel in [48]:
        df_small=df.loc[df["channel"]==channel]
        ax.errorbar(df_small["x"], df_small["y"], yerr=df_small["y_error"], xerr=df_small["x_error"],
                    linestyle='None',
                    marker="o",
                    #color="black",
                    markersize=0.1,
                    linewidth=0.5,
                    label=f"Channel:{channel}",
                   )

    #plt.xlim((500,600))
    plt.xlabel("Time [ns]")
    plt.ylabel("ADC Count")
    #plt.title("LED Flash, CERN 2022-03-27")
    plt.tight_layout()

    leg1 = ax.legend(borderpad=0.5, loc=1, ncol=1, frameon=True,facecolor="white",framealpha=1)
    leg1._legend_box.align = "left"
    leg1.set_title("SiPM Bias = 43.5 V")

    ax.grid(True)

    plt.savefig("./LEDsuperScan_10.pdf")
            
if __name__ == "__main__":
    
    #read()
    plot()
