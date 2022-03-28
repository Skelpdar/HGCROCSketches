from pfconfig import PFConfig

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
    c = PFConfig()
    if "general" in args.commands:
        c.set_general(board=args.board,rocs=[0,1,2],config="configs/march26_1400_LowBiasLEDFlash.yaml")
    elif "charge" in args.commands:
        c.set_charge_injection()
    elif "led" in args.commands:
        c.set_led(args.board,args.hdmi,args.sipm,args.led)
    elif "pscan" in args.commands:
        pulse_scan(c,args.odir)
    elif "sscan" in args.commands:
        pulse_l1a_scan(c,args.odir)
    c.run()

if __name__=="__main__":
    parser = argparse.ArgumentParser()
        parser.add_argument(
        '-c','--commands',
        dest="commands",
        nargs='+',
        choices=["general","charge","led","pscan","sscan"],
        help="Commands to run separated by spaces",
    )
    parser.add_argument(
        '-o','--odir',
        dest='odir',
        type=str,
        default='./data/'
        help='output directory that contains raw data e.g. ./data/led/'
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
    args = parser.parse_args()

    main(args)
