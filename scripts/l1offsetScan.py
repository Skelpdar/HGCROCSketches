import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import glob


#runs = list(range(49,78))
#values = list(range(8,124,4))

def read():

    listOfFiles = glob.glob(f"../data/l1scan/*.txt")
    #listOfFiles = glob.glob(f"../data/l1scan_80to90/*.txt")
    nsamples = 4
    theDict = {'x':[], 'x_error':[], 'y':[], 'y_error':[],'offset':[],'channel':[]}
    sampleDict = {'xx': [], 'yy': [], 'offset':[],'channel':[]}

    for currentFile in listOfFiles:
        half=int(currentFile.split(".")[2].split("/")[3].split("_")[1])
        if half != 1:
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

    # another big one
    df_sample = pd.DataFrame(sampleDict)
    df_sample = df_sample.sort_values(by=['xx'])
    df_sample.to_pickle("df_sample.pickle")


def plot():
    df = pd.read_pickle("df.pickle")
    pedestalDict = {}
    
    f, ax = plt.subplots(figsize=(25*(1/2.54), 13.875*(1/2.54)))
    for channel in range(0,37):
        df_small = df.loc[df["channel"]==channel]
        pedestal=np.mean(df_small["y"][:4])
        pedestalDict[str(channel)]=pedestal
        
        ax.errorbar(df_small["x"], df_small["y"]-pedestal,
                    yerr=df_small["y_error"], xerr=df_small["x_error"],
                    linestyle='None',
                    marker="o",
                    markersize=2,
                    linewidth=0.5,
                    label=f"Channel {channel}"
                    )
    plt.xlabel("L1AOffset [ns]")
    plt.ylabel("ADC Count")
    plt.title("L1AOffset Scan, CERN 2022-03-30")
    plt.tight_layout()
    leg1 = ax.legend(borderpad=0.5, loc=1, ncol=10, frameon=True,facecolor="white",framealpha=1,prop={'size': 6})
    leg1._legend_box.align = "left"
    leg1.set_title("DPM/Board/HCROC/HALF : 0/0/0/0\nSiPM Bias = 43.5 V")
    ax.grid(True)
    plt.savefig("./mean_per_channel.pdf")
    
#######################

    x=[]
    y=[]
    
    #df = pd.read_pickle("df_sample.pickle")
    df = pd.read_pickle("df.pickle")
    
    for index, row in df.iterrows():
        channel = str(int(row['channel']))
        diff = row['y']-pedestalDict[channel]
        if diff < 1:
            continue
        else:
            x.append(row['x'])
            y.append(row['y']-pedestalDict[channel])
    

    #df_sample = pd.read_pickle("df_sample.pickle")
    #x=np.array(df_sample["x"])
    #y=np.array(df_sample["y"])
    #print(y)
    
    x=np.array(x)
    y=np.array(y)
    
    x_min = 0
    x_max = 4000
      
    y_min = -2
    y_max = 25
      
    x_bins = np.linspace(x_min, x_max, 161)
    y_bins = np.linspace(y_min, y_max, 28)
      
    fig, ax = plt.subplots(figsize =(10, 7))
    # Creating plot
    plt.hist2d(x, y, bins =[x_bins, y_bins])
    plt.title("L1 Offset Scan, Pedestal Subtraction > 1 ADC")
      
    ax.set_xlabel('L1 Offset [ns]') 
    ax.set_ylabel('ADC Count') 
      
    # show plot
    plt.tight_layout()
    plt.savefig("./2D.pdf")
    #plt.show()

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
