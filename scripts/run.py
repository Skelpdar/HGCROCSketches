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

#./pflib/pfdecoder -r 0 -a ./data/led/0.raw | tee ./data/led/0.txt
#./pflib/pfdecoder -r 0 -a ./data/led/1.raw | tee ./data/led/1.txt
#./pflib/pfdecoder -r 0 -a ./data/led/2.raw | tee ./data/led/2.txt
#./pflib/pfdecoder -r 0 -a ./data/led/3.raw | tee ./data/led/3.txt
#./pflib/pfdecoder -r 0 -a ./data/led/4.raw | tee ./data/led/4.txt
#./pflib/pfdecoder -r 0 -a ./data/led/5.raw | tee ./data/led/5.txt
#./pflib/pfdecoder -r 0 -a ./data/led/6.raw | tee ./data/led/6.txt
#./pflib/pfdecoder -r 0 -a ./data/led/7.raw | tee ./data/led/7.txt
#./pflib/pfdecoder -r 0 -a ./data/led/8.raw | tee ./data/led/8.txt
#./pflib/pfdecoder -r 0 -a ./data/led/9.raw | tee ./data/led/9.txt
#./pflib/pfdecoder -r 0 -a ./data/led/10.raw | tee ./data/led/10.txt
#./pflib/pfdecoder -r 0 -a ./data/led/11.raw | tee ./data/led/11.txt
#./pflib/pfdecoder -r 0 -a ./data/led/12.raw | tee ./data/led/12.txt
#./pflib/pfdecoder -r 0 -a ./data/led/13.raw | tee ./data/led/13.txt
#./pflib/pfdecoder -r 0 -a ./data/led/14.raw | tee ./data/led/14.txt
#ls

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import glob


def main():

#    dac="10"
#    directory="./led_0/"
#    prefix="dac_"+dac+"_"

    directoryDict={
                    #"./charge/":{"legend":"LED Bias: 2500 DAC","color":"black"},
                    #"./led_2500/":{"legend":"LED Bias: 2500 DAC","color":"black"},
                    #"./regularScan_v2/":{"legend":"LED Bias: 2500 DAC","color":"black"},
                    "./data/":{"legend":".","color":"black"},
                    
                    
                    }

    f, ax = plt.subplots(figsize=(25*(1/2.54), 13.875*(1/2.54)))

    for key in directoryDict:
        directory=key
        
        listOfFiles = glob.glob(f"{directory}/*.txt")

#        listOfFiles = [ 
#                        directory+"0.txt",
#                        directory+"1.txt",
#                        directory+"2.txt",
#                        directory+"3.txt",
#                        directory+"4.txt",
#                        directory+"5.txt",
#                        directory+"6.txt",
#                        directory+"7.txt",
#                        directory+"8.txt",
#                        directory+"9.txt",
#                        directory+"10.txt",
#                        directory+"11.txt",
#                        directory+"12.txt",
#                        directory+"13.txt",
#                        directory+"14.txt",
#                        ]

        theDict = {'x':[], 'x_error':[], 'y':[], 'y_error':[],'offset':[]}
        
        x=[]
        y=[]
                     
        for currentFile in listOfFiles:
            #phase = int(currentFile.split(".")[1].split("/")[3].split("_")[1])
            #print(currentFile.split(".")[1].split("/")[2])
            half=int(currentFile.split(".")[1].split("/")[2].split("_")[1])
            if half != 0:
                continue
            offset = int(currentFile.split(".")[1].split("/")[2].split("_")[0])
            #print(offset)
            #sys.exit()
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
                if line[:3] == " 20":
                    currentData = line.split()
                    sample1.append(int(currentData[1]))
                    sample2.append(int(currentData[2]))
                    sample3.append(int(currentData[3]))
                    sample4.append(int(currentData[4]))

                    
                    y.append(int(currentData[1]))
                    x.append(0+offset*25)
                    y.append(int(currentData[2]))
                    x.append(25+offset*25)
                    y.append(int(currentData[3]))
                    x.append(50+offset*25)
                    y.append(int(currentData[4]))
                    x.append(75+offset*25)


            theDict["y"].append(float(np.mean(sample1)))
            theDict["y"].append(float(np.mean(sample2)))
            theDict["y"].append(float(np.mean(sample3)))
            theDict["y"].append(float(np.mean(sample4)))

            theDict["y_error"].append(float(np.std(sample1)))
            theDict["y_error"].append(float(np.std(sample2)))
            theDict["y_error"].append(float(np.std(sample3)))
            theDict["y_error"].append(float(np.std(sample4)))


            theDict["x"].append(0+offset*25)
            theDict["x"].append(25+offset*25)
            theDict["x"].append(50+offset*25)
            theDict["x"].append(75+offset*25)

                
            theDict["x_error"].append((25/16)/2)
            theDict["x_error"].append((25/16)/2)
            theDict["x_error"].append((25/16)/2)
            theDict["x_error"].append((25/16)/2)
            
            theDict['offset'].append(offset)
            theDict['offset'].append(offset)
            theDict['offset'].append(offset)
            theDict['offset'].append(offset)
            


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
    plt.title("Offset scan")
    plt.tight_layout()
    
    leg1 = ax.legend(borderpad=0.5, loc=1, ncol=1, frameon=True,facecolor="white",framealpha=1)
    leg1._legend_box.align = "left"
    leg1.set_title("SiPM Bias = 43.5 V")
    
    ax.grid(True)
    
    plt.savefig("./mean.pdf")

    #for offset in [84]:
    #    df_small=df.loc[df["offset"]==offset]
    ax.errorbar(x,y,
                linestyle='None',
                marker="o",
                color="black",
                markersize=2,
                linewidth=0.5,
                label=offset,
               )
        
    plt.xlabel("Time [ns]")
    plt.ylabel("ADC Count")
    plt.title("Offset Scan")
    plt.tight_layout()
    
    leg1 = ax.legend(borderpad=0.5, loc=1, ncol=2, frameon=True,facecolor="white",framealpha=1)
    leg1._legend_box.align = "left"
    leg1.set_title("SiPM Bias = 45V\n LED Bias = 8.9V")
    
    ax.grid(True)
    
    plt.savefig("./scatter.jpg")
    
if __name__ == "__main__":
    main()
