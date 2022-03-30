import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import glob


def read():

    listOfFiles = glob.glob(f"../data/l1scan/*.txt")
    nsamples = 4
    theDict = {'x':[], 'x_error':[], 'y':[], 'y_error':[],'offset':[],'channel':[]}
    sampleDict = {'xx': [], 'yy': [], 'offset':[],'channel':[]}

    for currentFile in listOfFiles:
        half=int(currentFile.split(".")[2].split("/")[3].split("_")[1])
        if half != 0:
            continue
        offset = int(currentFile.split(".")[2].split("/")[3].split("_")[0])
        with open(currentFile) as f:
            data = f.readlines()
            
        for channel in range(0,37):
            channelString = "  "+str(channel) if channel < 10 else " "+str(channel)

            samples = {}
            for i in range(nsamples):
                samples[str(i)] = []
            
            for line in data:
                if line[:3] == channelString:
                    currentData = line.split()
                    for i in range(nsamples):
                        samples[str(i)].append(int(currentData[i+1]))
                        sampleDict['xx'].append(int(currentData[i+1]))
                        sampleDict['yy'].append(i*25+offset*25)
                        sampleDict['offset'].append(offset)
                        sampleDict['channel'].append(int(channelString))
                        
            for i in range(nsamples):
                theDict["channel"].append(int(channelString))
                theDict["y"].append(float(np.mean(samples[str(i)])))
                theDict["y_error"].append(float(np.std(samples[str(i)])))
                theDict["x"].append(i*25+offset*25)
                theDict["x_error"].append((25/16)/2)
                theDict["offset"].append(offset)

    # big dataframe
    df = pd.DataFrame(theDict)
    df = df.sort_values(by=['x'])
    
    df = pd.DataFrame(theDict)
    df=df.sort_values(by=['x'])
    df.to_pickle("df.pickle")

#    # another big one
#    df_sample = pd.DataFrame(sampleDict)
#    df_sample = df_sample.sort_values(by=['xx'])

def plot():
    df = pd.read_pickle("df.pickle")  
    f, ax = plt.subplots(figsize=(25*(1/2.54), 13.875*(1/2.54)))
    for channel in range(0,37):
        df_small = df.loc[df["channel"]==channel]
        
        ax.errorbar(df_small["x"], df_small["y"],
                    yerr=df_small["y_error"], xerr=df_small["x_error"],
                    linestyle='None',
                    marker="o",
                    markersize=2,
                    linewidth=0.5,
                    label=f"Channel {channel}"
                    )
    plt.xlabel("Time [ns]")
    plt.ylabel("ADC Count")
    plt.title("Offset scan")
    plt.tight_layout()
    leg1 = ax.legend(borderpad=0.5, loc=1, ncol=1, frameon=True,facecolor="white",framealpha=1)
    leg1._legend_box.align = "left"
    leg1.set_title("SiPM Bias = 43.5 V")
    ax.grid(True)
    plt.savefig("./mean_per_channel.pdf")

#    f, ax = plt.subplots(figsize=(25*(1/2.54), 13.875*(1/2.54)))
#    for channel in range(0,37):
#        df_small = df_sample.loc[df["channel"]==channel]
#        ax.errorbar(
#            df_small["xx"],df_small["yy"],
#            linestyle='None',
#            marker="o",
#            markersize=2,
#            linewidth=0.5,
#            #label=offset,
#        )        
#    plt.xlabel("Time [ns]")
#    plt.ylabel("ADC Count")
#    plt.title("Offset Scan")
#    plt.tight_layout()
#    leg1 = ax.legend(borderpad=0.5, loc=1, ncol=2, frameon=True,facecolor="white",framealpha=1)
#    leg1._legend_box.align = "left"
#    leg1.set_title("SiPM Bias = 45V\n LED Bias = 8.9V")
#    ax.grid(True)
#    plt.savefig("./scatter_per_channel.jpg")
    
if __name__ == "__main__":
    if sys.argv[1] == "read":
        read()
    elif sys.argv[1] == "plot":
        plot()
