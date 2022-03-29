import argparse

def pulse_scan(c,output_dir):
    for phase in range(0,15):
        c.poke_param("top","phase",phase)
        c.daq_charge(nevents=100,output_name=f"{output_dir}/{phase}.raw")

def pulse_l1a_scan(c,output_dir):
    offsetList=[1,8,16,24,32,48,56,64,72,80,88,96,104]
    for offset in offsetList:
        c.fc_calib(offset)
        for phase in range(0,15):
            c.poke_param("top","phase",phase)
            c.daq_charge(nevents=100,output_name=f"{output_dir}/{offset}_{phase}.raw")

def main(args):
    import pfconfig
    with pfconfig.connect(f"cob1-dpm{args.dpm}") as c:
        if "general" in args.commands:
            print('Setting general commands')
            c.set_general(board=args.board,rocs=args.rocs,config=args.fconfig,l1a_offset=args.offset)
        elif "charge" in args.commands:
            print('Injecting charge')
            c.set_charge_injection()
            print('Saving daq charge')
            c.daq_charge(nevents=100,output_name=f"{args.odir}/100.raw")
        elif "nocharge" in args.commands:
            print('Disabling charge injection')
            c.set_charge_injection(off=True)
        elif "relink" in args.commands:
            print('Relink')
            c.elinks_reset()
            c.elinks_relink()
        elif "pedestal" in args.commands:
            print('Getting pedestal data')
            c.daq_pedestal(nevents=100,output_name=f"{args.odir}/100.raw")
        elif "led" in args.commands:
            print('Setting LED pulse')
            c.set_led(args.board,args.hdmi,args.sipm,args.led)
        elif "sipm" in args.commands:
            print('Setting BIAS')
            c.set_bias(args.board,args.hdmi,args.sipm)
        elif "pscan" in args.commands:
            print('DAQ with phase scan')
            pulse_scan(c,args.odir)
        elif "sscan" in args.commands:
            print('DAQ with phase and L1A offset scan')
            pulse_l1a_scan(c,args.odir)
        c.run(args.run)

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c','--commands',
        dest="commands",
        nargs='+',
        choices=["general",
                 "charge","nocharge",
                 "pedestal",
                 "led",
                 "pscan","sscan"],
        help="Commands to run separated by spaces",
    )
    parser.add_argument(
        '-o','--odir',
        dest='odir',
        type=str,
        default='./',
        help='output directory that contains raw data e.g. ./data/led/'
    )
    parser.add_argument(
        '--dpm',
        type=int,
        dest='dpm',
        default=1,
        help='DPM',
    )
    parser.add_argument(
        '--board',
        '-b',
        type=int,
        dest='board',
        default=0,
        help='Board ID',
    )
    parser.add_argument(
        '--rocs',
        type=int,
        nargs='+',
        dest='rocs',
        default=[0,1,2],
        help='ROCs (separated by spaces)',
    )
    parser.add_argument(
        '--hdmi',
        type=int,
        dest='hdmi',
        default=0,
        help='HDMI connector',
    )
    parser.add_argument(
        '--sipm',
        type=int,
        dest='sipm',
        default=3784,
        help='SiPM Bias',
    )
    parser.add_argument(
        '--led',
        type=int,
        dest='led',
        default=250,
        help='LED Bias',
    )
    parser.add_argument(
        '--offset',
        type=int,
        dest='offset',
        default=17,
        help='L1A offset',
    )
    parser.add_argument(
        '--fconfig',
        type=str,
        dest='fconfig',
        default="configs/march26_1400_LowBiasLEDFlash.yaml",
        help='Board ID',
    )
    parser.add_argument(
        '--run',
        action='store_true',
        dest='run',
        help='Run',
    )
    args = parser.parse_args()

    main(args)
