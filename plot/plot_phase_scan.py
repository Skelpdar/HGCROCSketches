import argparse
import pandas as pd
import glob
import matplotlib.pyplot as plt
import matplotlib.colors as clt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.image import NonUniformImage

def plot_pulse(fname,data,dpm=1,odir='./'):
    links = list(data["ILINK"].unique())
    phases = list(data["PHASE"].unique())
    channels = list(data["CHAN"].unique())
    samples = [col for col in data.columns if 'ADC' in col]
    i_samples = [int(s.replace('ADC','')) for s in samples]
    
    data_mean = data[samples+['CHAN','PHASE','ILINK']].groupby(['CHAN','PHASE','ILINK']).mean().reset_index()
    data_stderr = data[samples+['CHAN','PHASE','ILINK']].groupby(['CHAN','PHASE','ILINK']).std().reset_index()

    tag = fname.split('/')[-1].split('.')[0]
    pp = PdfPages(f'{tag}_phasescan.pdf')
    print(links)
    for ilink_counter,ilink in enumerate(links):
        for ch_counter,ch in enumerate(channels):
            phase_dict = {'time':[],'mean_adc':[],'time_error':[],'mean_error':[]}
            sample_dict = {
                'mean': {k: [] for k in i_samples},
                'error': {k: [] for k in i_samples},
            }

            for phase_counter,phase in enumerate(phases):
                adc_mean = data_mean.query(f"(CHAN=={ch}) & (ILINK=={ilink}) & (PHASE=={phase})")
                adc_stderr = data_stderr.query(f"(CHAN=={ch}) & (ILINK=={ilink}) & (PHASE=={phase})")
                for sample in samples:
                    s = int(sample.replace('ADC',''))
                    sample_dict['mean'][s].append(adc_mean[sample].to_numpy()[0])
                    sample_dict['error'][s].append(adc_stderr[sample].to_numpy()[0])
                    # print(phase,adc_mean[sample].to_numpy()[0],adc_stderr[sample].to_numpy()[0])
                    
            for s in i_samples:
                times = [s*25+(phase*(25/16)) for phase in phases]
                times_err = [(25/16)/2 for phase in phases]
                phase_dict["mean_adc"].extend(sample_dict['mean'][s])
                phase_dict["mean_error"].extend(sample_dict['error'][s])
                phase_dict["time"].extend(times)
                phase_dict["time_error"].extend(times_err)                

            fig, ax = plt.subplots(1,1,figsize=(25*(1/2.54), 13.875*(1/2.54)))
            ax.errorbar(phase_dict["time"],phase_dict["mean_adc"],
                        yerr=phase_dict["mean_error"],xerr=phase_dict["time_error"],
                        linestyle='None',
                        marker="o",
                        markersize=2,
                        linewidth=0.5,
                        label=f"Indiviual Charge Injection",
                        )
            ax.set_xlabel("Time [ns]")
            ax.set_ylabel("Mean ADC Count")
            ax.set_title(f"DPM {dpm} Link {ilink} Channel {ch}")
            leg1 = ax.legend(borderpad=0.5, loc=1, ncol=1, frameon=True,facecolor="white",framealpha=1)
            leg1._legend_box.align = "left"
            leg1.set_title("SiPM Bias = ? V")
            ax.grid(True)
            pp.savefig(fig)
            plt.close(fig)

    pp.close()

def main(arg):
    data = pd.read_csv(arg.fname)
    plot_pulse(arg.fname,data,arg.dpm,arg.odir)    
        
if __name__=="__main__":
    parser = argparse.ArgumentParser(f'python plot_scancharge.py ',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--fname',dest='fname',required=True,help='Filename with formatted scancharge data')
    parser.add_argument('--dpm',dest='dpm',type=int,required=True,help='DPM: 0 or 1?')
    parser.add_argument('-o','--odir',dest='odir',type=str,default='./',help='output directory for plots')
    arg = parser.parse_args()

    main(arg)
