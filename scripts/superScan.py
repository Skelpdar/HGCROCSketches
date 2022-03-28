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
        for offset in offsetList:
            for phase in phaseList:
                currentFile=f"./ledSuperScan_10_noLED/{offset}_{phase}.txt"
                #currentFile=f"./chargeSuperScan/{offset}_{phase}.txt"
                             
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
                    if channel < 10:
                        channelString="  "+str(channel)
                    else:
                        channelString=" "+str(channel)
                        
                    if line[:3] == channelString:
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
    #                    x.append(offset+0+(phase*(25/16)))
    #                    y.append(int(currentData[2]))
    #                    x.append(offset+25+(phase*(25/16)))
    #                    y.append(int(currentData[3]))
    #                    x.append(offset+50+(phase*(25/16)))
    #                    y.append(int(currentData[4]))
    #                    x.append(offset+75+(phase*(25/16)))
    #                    y.append(int(currentData[5]))
    #                    x.append(offset+100+(phase*(25/16)))
    #                    y.append(int(currentData[6]))
    #                    x.append(offset+125+(phase*(25/16)))
    #                    y.append(int(currentData[7]))
    #                    x.append(offset+150+(phase*(25/16)))
    #                    y.append(int(currentData[8]))
    #                    x.append(offset+175+(phase*(25/16)))

                theDict["channel"].append(int(channelString))
                theDict["channel"].append(int(channelString))
                theDict["channel"].append(int(channelString))
                theDict["channel"].append(int(channelString))
                theDict["channel"].append(int(channelString))
                theDict["channel"].append(int(channelString))
                theDict["channel"].append(int(channelString))
                theDict["channel"].append(int(channelString))

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

                theDict["x"].append(offset*25+0+(phase*(25/16)))
                theDict["x"].append(offset*25+25+(phase*(25/16)))
                theDict["x"].append(offset*25+50+(phase*(25/16)))
                theDict["x"].append(offset*25+75+(phase*(25/16)))
                theDict["x"].append(offset*25+100+(phase*(25/16)))
                theDict["x"].append(offset*25+125+(phase*(25/16)))
                theDict["x"].append(offset*25+150+(phase*(25/16)))
                theDict["x"].append(offset*25+175+(phase*(25/16)))
                    
                theDict["x_error"].append((25/16)/2)
                theDict["x_error"].append((25/16)/2)
                theDict["x_error"].append((25/16)/2)
                theDict["x_error"].append((25/16)/2)
                theDict["x_error"].append((25/16)/2)
                theDict["x_error"].append((25/16)/2)
                theDict["x_error"].append((25/16)/2)
                theDict["x_error"].append((25/16)/2)

    df = pd.DataFrame(theDict)
    df=df.sort_values(by=['x'])
    df.to_pickle("df.pickle")
    #pd.set_option('display.max_rows', 500)
    #print(df.loc[df["channel"]==0])
    #print(df)
  
def plot():
    f, ax = plt.subplots(figsize=(25*(1/2.54), 13.875*(1/2.54)))
    df = pd.read_pickle("df_original.pickle")
        
    for channel in [48]:
        df_small=df.loc[df["channel"]==channel]
        #print(df_small)
        ax.errorbar(df_small["x"], df_small["y"], yerr=df_small["y_error"], xerr=df_small["x_error"],
        #ax.errorbar(df["x"], df["y"], xerr=df["x_error"],
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
    #read()
    plot()
