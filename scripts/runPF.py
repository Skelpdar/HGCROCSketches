import argparse

def general_action(arg,c):
    print('Setting general commands')
    c.set_general(rocs=arg.rocs.split(','),config=arg.fconfig,l1a_offset=arg.offset)

def charge_action(arg,c):
    print(f'Enabling/Disabling charge injection for half {arg.half}',arg.coff)
    c.set_charge_injection(arg.rocs.split(','),off=arg.coff,half=arg.half,ch=arg.channel)
    if not arg.coff:
        print('Saving daq charge')
        c.daq_charge(nevents=arg.nevents,output_name=f"{arg.odir}/{arg.nevents}.raw")

def relink_action(arg,c):
    print('Relink')
    c.elinks_reset()
    c.elinks_relink()

def vref_action(arg,c):
    print(f'Setting vref {arg.value} for half {arg.half}',arg.rocs.split(','))
    c.roc_param(f"Reference_Voltage_{arg.half}","INV_VREF",arg.value,arg.rocs.split(','))

def l1offset_action(arg,c):
    print('Scanning over L1Offset for Halfs 0 and 1 and rocs',arg.rocs.split(','))
    values = arg.value.split(',')
    print(values)
    if len(values)==2:
        if arg.step:
            values = range(int(values[0]),int(values[1])+1,arg.step)
        else:
            values = range(int(values[0]),int(values[1])+1)
    print(values)
    for v in values:
        c.roc_param("Digital_Half_0","L1Offset",int(v),arg.rocs.split(','))
        c.roc_param("Digital_Half_1","L1Offset",int(v),arg.rocs.split(','))
        c.daq_external(nevents=arg.nevents)

def pedestal_action(arg,c):
    print('Getting pedestal data')
    c.daq_pedestal(nevents=arg.nevents,output_name=f"{arg.odir}/{arg.tag}{arg.nevents}.raw")

def hardreset_action(arg,c):
    print('Resync load')
    c.roc_resyncload(arg.rocs.split(','))

def led_action(arg,c):
    hdmis = arg.hdmi.split(',')
    print('Setting LED pulse for hdmis ',hdmis)
    for hdmi in hdmis:
        c.set_led(arg.rocs.split(','),int(hdmi),arg.sipm,arg.led)

def bias_action(arg,c):
    hdmis = arg.hdmi.split(',')
    print('Setting BIAS for hdmis ',hdmis)
    for hdmi in hdmis:
        c.set_bias(arg.board,int(hdmi),arg.sipm)

def l1aoffset_action(arg,c):
    print('Setting L1A offset')
    c.fc_calib(arg.offset)

def multisample_action(arg,c):
    print('Setting multisamples')
    c.fc_multisample(arg.value)
    
def pscan_action(arg,c):
    print('DAQ charge with phase scan')
    for phase in range(0,15):
        c.roc_param("top","phase",phase,arg.rocs.split(','))
        c.daq_charge(nevents=arg.nevents,output_name=f"{arg.odir}/{phase}.raw")

def sscan_action(arg,c):
    print('DAQ charge with phase and L1A offset scan')
    offsetList=[1,8,16,24,32,48,56,64,72,80,88,96,104]
    for offset in offsetList:
        c.fc_calib(offset)
        for phase in range(0,15):
            c.roc_param("top","phase",phase,arg.rocs.split('.'))
            c.daq_charge(nevents=arg.nevents,output_name=f"{output_dir}/{offset}_{phase}.raw")
            
if __name__=="__main__":
    parser = argparse.ArgumentParser(f'python runPF.py ',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--run',       action='store_true', dest='run',                 help='Run')
    parser.add_argument('--dpm',       type=int,            dest='dpm',    default=1,   help='DPM')
    parser.add_argument('--rocs',      type=str,            dest='rocs',   default='0', help='ROCs (separated by commas)')
    parser.add_argument('--hdmi',      type=str,            dest='hdmi',   default='0', help='HDMI connectors (separated by commas). Use -2 to run all connectors.')
    parser.add_argument('--nevents',   type=int,            dest='nevents',default=100, help='Number of events')
    subparsers = parser.add_subparsers(help='Choose which action to perform.')

    parse_general = subparsers.add_parser('general', help='Set general configuration')
    parse_general.add_argument('--fconfig',type=str,dest='fconfig',default="HGCROCSketches/configs/dpm1_board0_baseConfig.yaml",help='Config file')
    parse_general.add_argument('--offset',type=int,dest='offset',default=17,help='L1A offset')
    parse_general.set_defaults(action=general_action)

    parse_charge = subparsers.add_parser('charge', help='Charge daq')
    parse_charge.add_argument('--coff',action='store_true',dest='coff',help='Turn charge injection off')
    parse_charge.add_argument('--half',type=int,dest='half',default=0,help='Half')
    parse_charge.add_argument('--ch',type=int,dest='channel',default=0,help='Channel')
    parse_charge.add_argument('-o','--odir',dest='odir',type=str,default='.',help='output directory that contains raw data e.g. ./data/led/')
    parse_charge.set_defaults(action=charge_action)

    parse_relink = subparsers.add_parser('relink', help='Relink')
    parse_relink.set_defaults(action=relink_action)

    parse_vref = subparsers.add_parser('vref', help='Change inv vref')
    parse_vref.add_argument('--value',type=int,dest='value',default=0,help='Parameter value')
    parse_vref.add_argument('--half',type=int,dest='half',default=0,help='Half')
    parse_vref.set_defaults(action=vref_action)
    
    parse_l1offset = subparsers.add_parser('l1offset', help='Change l1offset')
    parse_l1offset.add_argument('--value',type=str,dest='value',default='0,1',help='Paremeter value or Range of parameter values split by commas')
    parse_l1offset.add_argument('--step',type=int,dest='step',default=1,help='Step in range of parameter values')
    parse_l1offset.set_defaults(action=l1offset_action)
    
    parse_pedestal = subparsers.add_parser('pedestal', help='Pedestal run')
    parse_pedestal.add_argument('-o','--odir',dest='odir',type=str,default='.',help='output directory that contains raw data e.g. ./data/led/')
    parse_pedestal.add_argument('--tag',dest='tag',type=str,default='',help='tag of output filename')
    parse_pedestal.set_defaults(action=pedestal_action)

    parse_led = subparsers.add_parser('led', help='LED pulse run')
    parse_led.add_argument('--sipm',type=int,dest='sipm',default=3784,help='SiPM Bias')
    parse_led.add_argument('--led',type=int,dest='led',default=0,help='LED Bias')
    parse_led.set_defaults(action=led_action)
    
    parse_bias = subparsers.add_parser('bias', help='Set LED or SiPM bias')
    parse_bias.add_argument('--sipm',type=int,dest='sipm',default=3784,help='SiPM Bias')
    parse_bias.set_defaults(action=bias_action)

    parse_l1aoffset = subparsers.add_parser('l1aoffset', help='Change l1aoffset in FC')
    parse_l1aoffset.add_argument('--offset',type=int,dest='offset',default=17,help='L1A offset')
    parse_l1aoffset.set_defaults(action=l1aoffset_action)

    parse_multisample = subparsers.add_parser('multisample', help='Change multisamples in FC')
    parse_multisample.add_argument('--value',type=int,dest='value',default=3,help='Multisample value')
    parse_multisample.set_defaults(action=multisample_action)

    parse_pscan = subparsers.add_parser('pscan', help='Pulse scan - changing phase')
    parse_pscan.add_argument('-o','--odir',dest='odir',type=str,default='./data/led/',help='output directory that contains raw data e.g. ./data/led/')
    parse_pscan.set_defaults(action=pscan_action)

    parse_sscan = subparsers.add_parser('sscan', help='Super scan - changing phase and L1A offset')
    parse_sscan.set_defaults(action=sscan_action)

    arg = parser.parse_args()

    # Each sub-command defines the 'action' member of the arg namespace
    # so if this member is not defined, no action has been selected
    if 'action' not in arg :
        parser.error('Must choose an action to perform!')

    import pfconfig
    with pfconfig.connect(f"cob1-dpm{arg.dpm}") as c:
        arg.action(arg,c)
        if arg.exit:
            c.write_exit()
        c.run(arg.run)
