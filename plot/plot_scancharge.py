import argparse
import pandas as pd
import glob
import matplotlib.pyplot as plt
import matplotlib.colors as clt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.image import NonUniformImage

def plot_pulse(data,dpm=1,odir='./'):
    links = list(data["ILINK"].unique())
    calib_dacs = list(data['CALIB_DAC'].unique())

    fig, axs = plt.subplots(len(links), len(calib_dacs))
    fig.suptitle('Channel vs sample, dpm1 charge injection (ILINK:CALIB_DAC)')
    
    for ilink_counter,ilink in enumerate(links):
        for calib_dac_counter,calib_dac in enumerate(calib_dacs):
            df = data.loc[data["CALIB_DAC"]==calib_dac]
            df = df.loc[df["ILINK"]==int(ilink)]
            df = df.groupby("CHAN").mean()
            
            x=[]
            y=[]
            weights=[]
            
            for index, row in df.iterrows():
                for sample in ["ADC0","ADC1","ADC2","ADC3"]:
                    x.append(int(sample[3]))
                    y.append(index)
                    weights.append(int(row[sample]))

            xmin = 0
            xmax = 4
            xedges = np.linspace(xmin, xmax, xmax+1)
            
            ymin = 0
            ymax = 36
            yedges = np.linspace(ymin, ymax, ymax+1)
            
            X, Y = np.meshgrid(xedges, yedges)
            H, xedges, yedges = np.histogram2d(x, y, bins=(xedges, yedges), weights=weights)
            # Histogram does not follow Cartesian convention, therefore transpose H for visualization purposes.
            H = H.T

            axs[ilink_counter, calib_dac_counter].pcolormesh(X, Y, H)
            axs[ilink_counter, calib_dac_counter].xaxis.set_ticks([0,1,2,3,4])
            axs[ilink_counter, calib_dac_counter].yaxis.set_ticks([0,18,36])
            axs[ilink_counter, calib_dac_counter].set_title(f"{ilink} : {calib_dac}")
            
    plt.tight_layout()
    plt.savefig(f"{odir}/pulses_dpm{dpm}.pdf")

def plot_calibdac_amplitude(data,dpm=1,odir='./'):
    samples = [f"ADC{i}" for i in range(4)]
    columns = samples + ['CALIB_DAC']
    data['AMP'] = data[samples].max(axis=1)

    calib_dacs = list(data['CALIB_DAC'].unique())
    lastval = calib_dacs[-1]
    calib_dacs.append(lastval+100)
    links = list(data["ILINK"].unique())
    
    import hist
    import mplhep as hep
    
    h_scan = hist.Hist(
        hist.axis.Variable(calib_dacs,name='calib_dac', label='CALIB DAC'),
        hist.axis.Regular(1024, 0, 1024, name='amplitude', label='Amplitude'),
        hist.axis.Regular(38, 0, 38, name='channel', label='Channel'),
        hist.axis.Regular(6, 0, 6, name='link', label='Link'),
    )
    
    h_scan.fill(
        calib_dac = data['CALIB_DAC'],
        amplitude = data['AMP'],
        channel = data['CHAN'],
        link = data['ILINK'],
    )

    for link in links:
        if dpm==0 and (link==2 or link==3):
            print('DPM0 has link 2,3 saved?')
            continue
        pp = PdfPages(f'{odir}/CALIBDAC_Amplitude_DPM{dpm}_link{link}.pdf')
        for ch in range(0,36,4):
            fig, ax = plt.subplots(1,4,figsize=(8*4, 6))
            for i in range(4):
                hep.hist2dplot(h_scan[{'channel': ch+i, 'link':link}], ax=ax[i], cmap="plasma", norm=clt.LogNorm(vmin=1e-3, vmax=1000))
                ax[i].set_title(f'Link {link} Channel {ch+i}')
            fig.tight_layout()
            fig.suptitle(f"CALIB DAC Scan Link {link} DPM {dpm}")
            pp.savefig(fig)
        pp.close()

def main(arg):
    data = pd.read_csv(arg.fname)
    plot_pulse(data,arg.dpm,arg.odir)
    plot_calibdac_amplitude(data,arg.dpm,arg.odir)
        
if __name__=="__main__":
    parser = argparse.ArgumentParser(f'python plot_scancharge.py ',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--fname',dest='fname',required=True,help='Filename with formatted scancharge data')
    parser.add_argument('--dpm',dest='dpm',type=int,required=True,help='DPM: 0 or 1?')
    parser.add_argument('-o','--odir',dest='odir',type=str,default='./',help='output directory for plots')
    arg = parser.parse_args()

    main(arg)
