import sys
import ROOT
from ROOT import TCanvas, TPad, TFile, TPaveLabel, TPaveText, TStyle, TTree, TH1D, TH2D, TLegend, TGraph, TGraphErrors
from ROOT import gROOT, gStyle, gSystem, gPad

gSystem.Load("libFramework.so")

inputFile=TFile(sys.argv[1], "read")
#baseName = sys.argv[1].replace('.root','')
#outputFile = f'hist_adc_{basename}.root'
outputFileName = 'time_adc_'+sys.argv[1]
tree=inputFile.Get("LDMX_Events")

f = ROOT.TFile(outputFileName,'recreate')

time = {}

for e in tree :

    for d in e.UMNChipSettingsTestDigis_unpack :

        #Create histogram if it does not already exist
        if d.id() not in time :
           #h[d.id()] = ROOT.TH1F(f'adc_eid_{d.id()}', f'ADC EID {d.id()}',1024,0,1024)
           #hmax[d.id()] = ROOT.TH1F(f'max_adc_eid_{d.id()}', f'MAX ADC EID {d.id()}',1024,0,1024)
           time[d.id()] = ROOT.TH2F(f'pulse_eid_{d.id()}', f'PULSE ADC EID {d.id()}', 8,0,8,1024,0,1024)

        #Find maximum ADC count out of all time samples
        #maximumADC = max([d.at(i).adc_t() for i in range(d.size())])
        #hmax[d.id()].Fill(maximumADC)       
 
        #Iterate through samples
        for i in range(d.size()) :

           time[d.id()].Fill(i,d.at(i).adc_t())

#fitFunc = ROOT.TF1("fitFunc","gaus");
#for channel in h :
#    print(channel)
#    hist = h[channel]
#    peak = hist.GetBinCenter(hist.GetMaximumBin())
#    fitFunc.SetParameter(1,peak);
#    hist.Fit(fitFunc,"SQ","",peak-15,peak+15)
#    print('%s, %.1f, %.1f' % (channel,peak,fitFunc.GetParameter(1)))
#    print('%s, %.1f, %.1f' % (channel,peak,hist.GetStdDev()))

f.Write()
f.Close()
