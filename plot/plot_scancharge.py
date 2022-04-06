import argparse
import pandas as pd
import glob
import matplotlib.pyplot as plt
import matplotlib.colors as clt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.image import NonUniformImage

def plot_pulse(fname,data,dpm=1,odir='./'):
    print(data)
    links = list(data["ILINK"].unique())
    calib_dacs = list(data['CALIB_DAC'].unique())


    
    fig = plt.figure(figsize=(8.27, 11.69), dpi=100)
    fig.suptitle(f'dpm{dpm} Charge Injection')
    gs = fig.add_gridspec(len(links), len(calib_dacs), hspace=0.2, wspace=0.05)
    axs = gs.subplots(sharex='col', sharey='row')
    
    print(axs[0][0])
    
    for ilink_counter,ilink in enumerate(links):
        for calib_dac_counter,calib_dac in enumerate(calib_dacs):
            df = data.loc[data["CALIB_DAC"]==calib_dac]
            df = df.loc[df["ILINK"]==int(ilink)]
            df = df.groupby("CHAN").mean()
            
            x=[]
            y=[]
            weights=[]
            
            for index, row in df.iterrows():
                for sample in ["ADC0","ADC1","ADC2","ADC3","ADC4","ADC5","ADC6","ADC7"]:
                    x.append(int(sample[3]))
                    y.append(index)
                    weights.append(int(row[sample]))

            xmin = 0
            xmax = 8
            xedges = np.linspace(xmin, xmax, xmax+1)
            
            ymin = 0
            ymax = 36
            yedges = np.linspace(ymin, ymax, ymax+1)
            
            X, Y = np.meshgrid(xedges, yedges)
            H, xedges, yedges = np.histogram2d(x, y, bins=(xedges, yedges), weights=weights)
            H = H.T

            print(ilink_counter,calib_dac_counter)
            c = axs[ilink_counter][calib_dac_counter].pcolormesh(X, Y, H, vmin=0, vmax=600)
            axs[ilink_counter][calib_dac_counter].xaxis.set_ticks([0,1,2,3,4,5,6,7,8])
            axs[ilink_counter][calib_dac_counter].yaxis.set_ticks([0,18,36])
            
            if ilink_counter == 0:
                ax = axs[ilink_counter][calib_dac_counter].twiny()
                ax.set_xlabel(f"Charge Strength: {calib_dacs[calib_dac_counter]} [DAC]")
                ax.set_xticklabels([])
            if calib_dac_counter == len(calib_dacs)-1:
                ax = axs[ilink_counter][calib_dac_counter].twinx()
                ax.set_ylabel(f"Elink: {ilink}")
                ax.tick_params(axis='y', pad=60)
                ax.set_yticklabels([])
            if ilink_counter == len(links)-1:
                axs[ilink_counter][calib_dac_counter].set_xlabel(f"Time Sample")
            if calib_dac_counter == 0:
                axs[ilink_counter][calib_dac_counter].set_ylabel(f"Channel")
            if calib_dac_counter == len(calib_dacs)-1:
                fig.colorbar(c, ax=axs[ilink_counter][calib_dac_counter])
                
    plt.tight_layout()
    plt.savefig(f"{odir}/{fname.split('/')[-1].split('.')[0]}.pdf")

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
    plot_pulse(arg.fname,data,arg.dpm,arg.odir)
    #plot_calibdac_amplitude(data,arg.dpm,arg.odir)
        
if __name__=="__main__":
    parser = argparse.ArgumentParser(f'python plot_scancharge.py ',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--fname',dest='fname',required=True,help='Filename with formatted scancharge data')
    parser.add_argument('--dpm',dest='dpm',type=int,required=True,help='DPM: 0 or 1?')
    parser.add_argument('-o','--odir',dest='odir',type=str,default='./',help='output directory for plots')
    arg = parser.parse_args()

    main(arg)
