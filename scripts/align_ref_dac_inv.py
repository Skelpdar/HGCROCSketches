"""
Automatic pedestal alignment of the channel-wise pre-amplifier parameter ref_dac_inv

Input: Digis from a pedestal measurement, with ref_dac_inv = 0 and dacb = 0 on all channels. The shaper parameters Inv_vref and Noinv_vref can be tuned to set all pedestals to approximately ~50 ticks, with a lot of spread.

Output: A new .yaml config file with channel-wise ref_dac_inv adjustment

Example usage: ldmx python3 align_ref_dac_inv.py unpacked_untunedPedestals.root newConfigFile.yaml

Currently it reads from the first two connected links only

For small ADC counts, the relationship between ref_dac_inv and pedestal is linear and approximately:

dPedestal = dRef_dac_inv * 6.3

Author: Erik
"""

import sys
import ROOT
from ROOT import TCanvas, TPad, TFile, TPaveLabel, TPaveText, TStyle, TTree, TH1D, TH2D, TLegend, TGraph, TGraphErrors
from ROOT import gROOT, gStyle, gSystem, gPad

gSystem.Load("libFramework.so")

inputFile=TFile(sys.argv[1], "read")
outputConfigFile = open(sys.argv[2], "w")

tree=inputFile.Get("LDMX_Events")

h = {}

for e in tree :

    for d in e.UMNChipSettingsTestDigis_unpack :

        #Create histogram if it does not already exist
        if d.id() not in h :

           h[d.id()] = ROOT.TH1F(f'adc_eid_{d.id()}', f'ADC EID {d.id()}',1024,0,1024)
 
        #Iterate through samples
        for i in range(d.size()) :
            h[d.id()].Fill(d.at(i).adc_t())

#Find pedestal values by a Gaussian fit
pedestals = []
fitFunc = ROOT.TF1("fitFunc","gaus");
for channel in h :
    hist = h[channel]
    peak = hist.GetBinCenter(hist.GetMaximumBin())
    fitFunc.SetParameter(1,peak);
    hist.Fit(fitFunc,"SQ","",peak-15,peak+15)
    pedestals.append(fitFunc.GetParameter(1))

#Mapping from row in data to Channel number pagename
channelMapping = {
    0:"CHANNEL_0",
    1:"CHANNEL_1",
    2:"CHANNEL_2",
    3:"CHANNEL_3",
    4:"CHANNEL_4",
    5:"CHANNEL_5",
    6:"CHANNEL_6",
    7:"CHANNEL_7",
    8:"CHANNEL_8",
    9:"CHANNEL_9",
    10:"CHANNEL_10",
    11:"CHANNEL_11",
    12:"CHANNEL_12",
    13:"CHANNEL_13",
    14:"CHANNEL_14",
    15:"CHANNEL_15",
    16:"CHANNEL_16",
    17:"CHANNEL_17",
    19:"CHANNEL_18",
    20:"CHANNEL_19",
    21:"CHANNEL_20",
    22:"CHANNEL_21",
    23:"CHANNEL_22",
    24:"CHANNEL_23",
    25:"CHANNEL_24",
    26:"CHANNEL_25",
    27:"CHANNEL_26",
    28:"CHANNEL_27",
    29:"CHANNEL_28",
    30:"CHANNEL_29",
    31:"CHANNEL_30",
    32:"CHANNEL_31",
    33:"CHANNEL_32",
    34:"CHANNEL_33",
    35:"CHANNEL_34",
    36:"CHANNEL_35",
    37:"CHANNEL_36",    
    38:"CHANNEL_37",    
    39:"CHANNEL_38",    
    40:"CHANNEL_39",    
    41:"CHANNEL_40",    
    42:"CHANNEL_41",    
    43:"CHANNEL_42",    
    44:"CHANNEL_43",    
    45:"CHANNEL_44",    
    46:"CHANNEL_45",    
    47:"CHANNEL_46",    
    48:"CHANNEL_47",    
    49:"CHANNEL_48",    
    50:"CHANNEL_49",    
    51:"CHANNEL_50",    
    52:"CHANNEL_51",    
    53:"CHANNEL_52",    
    54:"CHANNEL_53",    
    56:"CHANNEL_54",    
    57:"CHANNEL_55",    
    58:"CHANNEL_56",    
    59:"CHANNEL_57",    
    60:"CHANNEL_58",    
    61:"CHANNEL_59",    
    62:"CHANNEL_60",    
    63:"CHANNEL_61",    
    64:"CHANNEL_62",    
    65:"CHANNEL_63",    
    66:"CHANNEL_64",    
    67:"CHANNEL_65",    
    68:"CHANNEL_66",    
    69:"CHANNEL_67",    
    70:"CHANNEL_68",    
    71:"CHANNEL_69",    
    72:"CHANNEL_70",    
    73:"CHANNEL_71"    
}

for i,l in enumerate(pedestals):
    #Only look at two links
    if i < 74:
        #Ignore non-physical channels
        if i in [18,55]:
            pass
        else:
            pagename = channelMapping[i]
            print(pagename + ":\n")
            outputConfigFile.write(pagename+":\n")
            
            #Calculate new ref_dac_inv
            new_ref_dac_inv = (100-l)/6.3
            
            print("  Ref_dac_inv: " + str(min(max(0,int(new_ref_dac_inv)),31))+"\n")
            outputConfigFile.write("  Ref_dac_inv: " + str(min(max(0,int(new_ref_dac_inv)),31))+"\n")

close(outputConfigFile)
